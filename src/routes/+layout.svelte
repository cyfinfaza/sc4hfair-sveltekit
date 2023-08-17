<script>
	import { browser } from '$app/environment';
	import { afterNavigate } from '$app/navigation';
	import { updated } from '$app/stores';
	import { onMount, setContext } from 'svelte';
	import Modal from 'components/Modal.svelte';
	import { pvtUpdate, pushPoprxUpdate, startPoprx } from 'logic/analytics.js';

	import 'styles/global.css';
	import 'styles/material-icons.css';
	import 'styles/fonts.css';

	export let data;
	setContext('sponsors', data?.sponsors || []);

	/** @type {ServiceWorkerRegistration|undefined} */
	let swRegistration;
	// const skipWaiting = () => swRegistration?.waiting?.postMessage({ type: 'SKIP_WAITING' }); // ask for the new sw to take over & reload us

	let controllerChangeOccurred = false;

	$: {
		if ($updated && swRegistration) {
			swRegistration.update();
		}
	}

	onMount(async () => {
		if (!browser) return;

		swRegistration = await navigator.serviceWorker.getRegistration();
		if (!swRegistration) return;

		// new sw has taken over
		const onControllerChange = () => (controllerChangeOccurred = true);
		navigator.serviceWorker.ready.then(() => {
			navigator.serviceWorker.addEventListener('controllerchange', onControllerChange);
		});

		// // always force update if possible
		// if (dev) skipWaiting();

		// // https://whatwebcando.today/articles/handling-service-worker-updates/

		// const handleSwUpdate = () => {
		// 	console.log('service worker update detected!');
		// 	swRegistration.installing.addEventListener(
		// 		'statechange',
		// 		() => {
		// 			if (dev) skipWaiting();
		// 			if (swRegistration.waiting && navigator.serviceWorker.controller) {
		// 				// there's an old sw running and a new sw waiting to install
		// 				// let sveltekit decide if we need to show the proompt
		// 				updated.check();
		// 				// then in the prompt, we will ask to go through with the update or wait for it to happen naturally
		// 			}
		// 		},
		// 		{ once: true }
		// 	);
		// };
		// swRegistration.addEventListener('updatefound', handleSwUpdate);

		() => {
			// cleanup
			// swRegistration?.removeEventListener('updatefound', handleSwUpdate);
			navigator.serviceWorker.removeEventListener('controllerchange', onControllerChange);
		};
	});

	afterNavigate(() => {
		console.log('afterNavigate', window.location.pathname);
		try {
			pvtUpdate();
		} catch (error) {
			console.error('pvt error:', error);
		}
	});
	onMount(() => {
		let client = startPoprx('wss://fair-app-poprx.4hcomputers.club');
		document.addEventListener('visibilitychange', (e) => {
			if (
				document.visibilityState === 'visible' &&
				(!client || client.readyState === 2 || client.readyState === 3)
			)
				client = startPoprx('wss://fair-app-poprx.4hcomputers.club');
			else client.close();
		});
		return () => {
			client.close();
		};
		// start_poprx('ws://localhost:6002');
	});

	// force reload on navigation if app can be updated,
	// including when the app initially loads
	// disabling because this causes an infinite reload loop????
	// beforeNavigate(async ({ to, willUnload }) => {
	// 	if ((await updated.check()) && !willUnload && to?.url) {
	// 		skipWaiting();
	// 		location.href = to.url.href;
	// 	}
	// });
</script>

<svelte:window
	on:error={(e) => {
		e.preventDefault();
		console.error(e, e.error);
	}}
	on:unhandledrejection={(e) => {
		e.preventDefault();
		console.error(e);
	}}
/>

<slot />

<Modal
	show={controllerChangeOccurred}
	on:confirm={() => window.location.reload()}
	closeText="Later"
	confirmText="Refresh now"
>
	<h2>New version ready</h2>
	<p>A new version of the app has been downloaded. Refresh now to load the new version.</p>
</Modal>
