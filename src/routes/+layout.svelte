<script>
	import { browser } from '$app/environment';
	import { beforeNavigate } from '$app/navigation';
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

	onMount(async () => {
		if (!browser) return;
		// https://whatwebcando.today/articles/handling-service-worker-updates/
		swRegistration = await navigator.serviceWorker.getRegistration();
		if (!swRegistration) return;

		const handleSwUpdate = () => {
			console.log('service worker update detected!');
			swRegistration.installing.addEventListener(
				'statechange',
				() => {
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

		() => {
			// cleanup
			swRegistration?.removeEventListener('updatefound', handleSwUpdate);
		};
	});

	const skipWaiting = () => swRegistration?.waiting?.postMessage({ type: 'SKIP_WAITING' }); // ask for the new sw to take over & reload us

	// force reload on navigation if app can be updated
	beforeNavigate(({ willUnload, to }) => {
		if ($updated && !willUnload && to?.url) {
			skipWaiting();
			location.href = to.url.href;
		}
	});
</script>

<slot />

<Modal show={$updated} on:confirm={skipWaiting}>
	<p>New version of the app is available. Refresh now?</p>
</Modal>
