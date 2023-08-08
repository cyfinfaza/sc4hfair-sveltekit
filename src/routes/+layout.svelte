<script>
	import { browser, dev } from '$app/environment';
	import { afterNavigate, beforeNavigate } from '$app/navigation';
	import { updated } from '$app/stores';
	import { onMount, setContext } from 'svelte';
	import Modal from 'components/Modal.svelte';

	import 'styles/global.css';
	import 'styles/material-icons.css';
	import 'styles/fonts.css';

	export let data;
	setContext('sponsors', data?.sponsors || []);

	/** @type {ServiceWorkerRegistration|undefined} */
	let swRegistration;
	const skipWaiting = () => swRegistration?.waiting?.postMessage({ type: 'SKIP_WAITING' }); // ask for the new sw to take over & reload us

	onMount(async () => {
		if (!browser) return;

		swRegistration = await navigator.serviceWorker.getRegistration();
		if (!swRegistration) return;

		// always force update if possible
		if (dev) skipWaiting();

		// https://whatwebcando.today/articles/handling-service-worker-updates/

		const handleSwUpdate = () => {
			console.log('service worker update detected!');
			swRegistration.installing.addEventListener(
				'statechange',
				() => {
					if (dev) skipWaiting();
					if (swRegistration.waiting && navigator.serviceWorker.controller) {
						// there's an old sw running and a new sw waiting to install
						// let sveltekit decide if we need to show the proompt
						updated.check();
						// then in the prompt, we will ask to go through with the update or wait for it to happen naturally
					}
				},
				{ once: true }
			);
		};
		swRegistration.addEventListener('updatefound', handleSwUpdate);

		// new sw has taken over
		// const reload = () => location.reload();
		// navigator.serviceWorker.ready.then(() => {
		// 	navigator.serviceWorker.addEventListener('controllerchange', reload);
		// });

		() => {
			// cleanup
			swRegistration?.removeEventListener('updatefound', handleSwUpdate);
			// navigator.serviceWorker.removeEventListener('controllerchange', reload);
		};
	});

	// force reload on navigation if app can be updated,
	// including when the app initially loads
	beforeNavigate(async ({ to, willUnload }) => {
		if ((await updated.check()) && !willUnload && to?.url) {
			skipWaiting();
			location.href = to.url.href;
		}
	});
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

<slot data-sveltekit-reload={true} />

<Modal show={$updated} on:confirm={skipWaiting} closeText="Later" confirmText="Load now">
	<h2>New version available</h2>
	<p>A new version of the app is available. Load the new version now?</p>
</Modal>
