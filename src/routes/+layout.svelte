<script>
	import { browser, version } from '$app/environment';
	import { afterNavigate, replaceState } from '$app/navigation';
	import { updated } from '$app/stores';
	import KioskPitch from 'components/KioskPitch.svelte';
	import Modal from 'components/Modal.svelte';
	import { pvtUpdate } from 'logic/pvt.js';
	import { kioskMode } from 'logic/stores.js';
	import { canWebShare } from 'logic/webshare.js';
	import { onMount, setContext } from 'svelte';

	import 'styles/fonts.css';
	import 'styles/global.css';
	import 'styles/material-icons.css';

	export let data;
	setContext('sponsors', data?.sponsors || []);

	/** @type {ServiceWorkerRegistration | undefined} */
	let swRegistration;
	// const skipWaiting = () => swRegistration?.waiting?.postMessage({ type: 'SKIP_WAITING' }); // ask for the new sw to take over & reload us

	let controllerChangeOccurred = false;
	let newVersionVerified = false;
	$: {
		if (controllerChangeOccurred) {
			console.log('controller change occurred, verifying new version');
			fetch('/_app/version.json', {
				cache: 'no-cache',
				headers: { 'Cache-Control': 'no-cache' },
			})
				.then((res) => res.json())
				.then((versionData) => {
					if (versionData.version !== version) {
						newVersionVerified = true;
					}
				})
				.catch((e) => console.error('failed to verify new version', e));
		}
	}

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

	/** @type {() => void | undefined} */
	let pushPoprxUpdate;
	afterNavigate(({ to }) => {
		const href = to?.url.href;
		console.log('afterNavigate', href);

		const kioskSwitch = to?.url.searchParams.get('kiosk');
		if (kioskSwitch === 'enable') $kioskMode = true;
		else if (kioskSwitch === 'disable') $kioskMode = false;

		const referrer = to?.url.searchParams.get('referrer');

		if (to && (kioskSwitch || referrer)) replaceState(to.url.pathname, {});

		if (typeof pushPoprxUpdate === 'function') pushPoprxUpdate();

		try {
			pvtUpdate({ href, referrer });
		} catch (error) {
			console.error('pvt error:', error);
		}
	});

	onMount(() => {
		/** @param {string} addr */
		function start_poprx(addr) {
			let txid = window.localStorage.getItem('poprx-txid');
			if (!txid) {
				txid = (Math.floor(Math.random() * 900000) + 100000).toString();
				window.localStorage.setItem('poprx-txid', txid);
			}
			const client = new WebSocket(addr);
			// client.onmessage = function (event) {
			// 	const data = JSON.parse(event.data);
			// 	console.log('poprx:', data);
			// };
			client.onopen = function () {
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
		document.addEventListener('visibilitychange', () => {
			if (
				document.visibilityState === 'visible' &&
				(!client ||
					client.readyState === WebSocket.CLOSING ||
					client.readyState === WebSocket.CLOSED)
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

	$: $canWebShare = browser && 'share' in navigator && !$kioskMode;

	/** @type {Modal} */
	let externalLinkModal;
</script>

<svelte:window
	on:error={(e) => {
		e.preventDefault();
		console.error(e, e.error);
		if (parseInt(localStorage.getItem('lastError') || '') - Date.now() < 1000) {
			// just crashed and reloaded, prevent reload loop
		} else {
			window.location.reload();
		}
		localStorage.setItem('lastError', Date.now().toString());
	}}
	on:unhandledrejection={(e) => {
		e.preventDefault();
		console.error(e);
		if (parseInt(localStorage.getItem('lastError') || '') - Date.now() < 1000) {
			// just crashed and reloaded, prevent reload loop
		} else {
			window.location.reload();
		}
		localStorage.setItem('lastError', Date.now().toString());
	}}
	on:click={(e) => {
		const target = e.target instanceof Element && e.target.closest('a');
		if (!target) return;
		console.log('hi');
		// const url = new URL(target.href, window.location.origin);
		// if (url.origin !== window.location.origin) {
		// 	e.preventDefault();
		// 	externalLinkModal.showModal();
		// }
	}}
/>

<slot />

<Modal
	show={newVersionVerified}
	on:confirm={() => window.location.reload()}
	closeText="Later"
	confirmText="Refresh now"
>
	<h2>New version ready</h2>
	<p>A new version of the app has been downloaded. Refresh now to load the new version.</p>
</Modal>

<Modal show={false} bind:this={externalLinkModal} confirmation={false} closeText="Cancel">
	<div class="center">
		<KioskPitch box={false}>
			<h2 style="margin-top: 0;">Visiting External Link</h2>
			<p>You can't exit the app in the kiosk, try on your own device!</p>
		</KioskPitch>
	</div>
</Modal>
