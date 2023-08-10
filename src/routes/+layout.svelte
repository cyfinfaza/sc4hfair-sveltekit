<script>
	import { browser, dev } from '$app/environment';
	import { afterNavigate, beforeNavigate } from '$app/navigation';
	import { updated } from '$app/stores';
	import { onMount, setContext } from 'svelte';
	import Modal from 'components/Modal.svelte';
	import { checkIsStandalone } from 'logic/platform.js';

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

	function pvtUpdate() {
		let requestBody = JSON.stringify({
			url: window.location.href,
			meta: {
				standalone: checkIsStandalone(),
				sh_2023_code: localStorage.getItem('sh_2023_code') || undefined,
			},
		});
		fetch('/api/pvt', {
			method: 'POST',
			body: requestBody,
			credentials: 'include',
			type: 'application/json',
		}).then((response) =>
			response.text().then((status) => {
				console.log('track:', status);
				if (status === 'unconfirmed') {
					fetch('/api/pvt', {
						method: 'POST',
						body: requestBody,
						credentials: 'include',
						type: 'application/json',
					});
				}
			})
		);
	}

	let pushPoprxUpdate;
	afterNavigate(() => {
		console.log('afterNavigate', window.location.pathname);
		if (typeof pushPoprxUpdate === 'function') pushPoprxUpdate();
		try {
			pvtUpdate();
		} catch (error) {
			console.error('pvt error:', error);
		}
	});
	onMount(() => {
		function start_poprx(addr) {
			let txid = window.localStorage.getItem('poprx-txid');
			if (!txid) {
				txid = Math.floor(Math.random() * 900000) + 100000;
				window.localStorage.setItem('poprx-txid', txid);
			}
			const client = new WebSocket(addr);
			client.onmessage = function (event) {
				const data = JSON.parse(event.data);
				console.log('poprx:', data);
			};
			client.onopen = function (event) {
				client.send(
					JSON.stringify({
						type: 'txinit',
						data: { id: txid, agent: navigator.userAgent, path: window.location.pathname },
					})
				);
				pushPoprxUpdate = () => {
					try {
						client.send(
							JSON.stringify({
								type: 'pathupdate',
								data: { id: txid, path: window.location.pathname },
							})
						);
					} catch (error) {
						console.error('poprx error:', error);
					}
				};
			};
			return client;
		}
		let client = start_poprx('wss://fair-app-poprx.4hcomputers.club');
		document.addEventListener('visibilitychange', (e) => {
			if (
				document.visibilityState === 'visible' &&
				(!client || client.readyState === 2 || client.readyState === 3)
			)
				client = start_poprx('wss://fair-app-poprx.4hcomputers.club');
			else client.close();
		});
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
