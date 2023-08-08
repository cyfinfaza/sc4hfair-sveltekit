/// <reference types="@sveltejs/kit" />
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />
const sw = /** @type {ServiceWorkerGlobalScope} */ (/** @type {unknown} */ (self));

import { build, files, prerendered, version } from '$service-worker';

const CACHE_NAME = 'offline-cache-v2';
const PRECACHE = ['/_app/version.json', ...build, ...files, ...prerendered];

// console.log('precache: ', PRECACHE);
console.log('SW VERSION: ', version);

sw.addEventListener('install', (event) => {
	// sw.skipWaiting();
	console.log('Service worker installing');
	event.waitUntil(
		(async () => {
			const cache = await caches.open(CACHE_NAME);

			console.log('PRECACHE SIZE', PRECACHE.length);

			let toCache = PRECACHE;
			const existingKeys = await cache.keys();

			for (const req of existingKeys) {
				const url = new URL(req.url),
					immutable = url.pathname.startsWith('/_app/immutable');
				if (immutable && toCache.includes(url.pathname)) {
					// immutable files are hashed, we can skip caching them again
					toCache.splice(toCache.indexOf(url.pathname), 1);
				}
			}

			console.log('PRECACHE SIZE REDUCED TO', toCache.length);

			try {
				await cache.addAll(toCache);
				console.log('PRECACHE COMPLETE');
			} catch (e) {
				console.log('PRECACHE FAILED: ', e);
			}

			if (await caches.has('offline-cache-v1')) {
				console.log('HOSTILE TAKEOVER OF APP V1');
				await sw.skipWaiting();
			}
		})()
	);
});

sw.addEventListener('message', (event) => {
	if (event?.data?.type === 'SKIP_WAITING') {
		sw.skipWaiting(); // install new sw (update caches), then activate (reload old versions)
	}
});

sw.addEventListener('activate', (event) => {
	console.log('SW ACTIVATED');
	event.waitUntil(
		// we can do all of these maintenance tasks in parallel
		Promise.allSettled([
			sw.clients.claim(),

			(async () => {
				// ensure we are never running any old versions
				// after we've taken over, iterate over all the current clients (windows)
				const tabs = await sw.clients.matchAll({ type: 'window' });
				tabs.forEach((tab) => {
					// and refresh each one of them
					tab.navigate(tab.url);
				});
			})(),

			// does this work?
			(async () => {
				const cache = await caches.open(CACHE_NAME);
				let toUncache = [];
				for (const req of await cache.keys()) {
					const url = new URL(req.url);
					if (url.origin === location.origin && !PRECACHE.includes(url.pathname)) {
						// we can remove them from the cache if they are no longer in the precache
						toUncache.push(req.url);
						await cache.delete(req);
					}
				}
				console.log('UNCACHED', toUncache.length, 'OLD FILES', toUncache);
			})(),

			// remove old cache from v1 of the app
			caches.delete('offline-cache-v1'),
		])
	);
});

/** @param {FetchEvent} event */
function cacheFirst(event, revalidateEtag = false) {
	event.respondWith(
		(async function () {
			const cache = await caches.open(CACHE_NAME);
			const cachedResponse = await cache.match(event.request, { ignoreSearch: true }); // `?x-sveltekit-invalidated=01`
			console.log(cachedResponse);
			if (cachedResponse) {
				const cacheEtag = cachedResponse.headers.get('etag');
				console.log('CACHED: ', cachedResponse.url, cacheEtag);
				let wasRevalidated = false;
				if (revalidateEtag) {
					event.waitUntil(
						(async () => {
							const headRequest = await fetch(event.request.url, { method: 'HEAD' });
							const headEtag = headRequest.headers.get('etag');
							console.log('REVALIDATE HEAD CHECK: ', cachedResponse.url, cacheEtag);
							if (headEtag && cacheEtag !== headEtag) {
								console.log('REVALIDATING: ', cachedResponse.url);
								await cache.delete(event.request);
								const newReq = await fetch(event.request);
								if (newReq.ok) await cache.put(event.request, newReq.clone());
								else console.log('REVALIDATE NOT OK: ', newReq);
								wasRevalidated = true; // regrab the response from the cache
							}
						})()
					);
				}
				return wasRevalidated
					? await cache.match(event.request, { ignoreSearch: true })
					: cachedResponse;
			} else {
				console.log('CACHE MISS: ', event.request.url);
				let resp;
				try {
					resp = await fetch(event.request);
				} catch (e) {
					console.log('FETCH ERROR: ', e);
					// this is broken as sveltekit's routing doesn't trigger this
					// we could hook into the router and force the navigation if we wanted
					// (https://github.com/sveltejs/kit/issues/2570 for some reference)
					// this page is only for when something goes really wrong
					// as all real pages in the app should already have offline support
					if (event.request.mode === 'navigate') return cache.match('/offline');
					else return resp;
				}
				if (resp.ok) event.waitUntil(cache.put(event.request, resp.clone()));
				else console.log('FETCH NOT OK: ', resp);
				return resp;
			}
		})()
	);
}

/** @param {FetchEvent} event */
function networkFirst(event) {
	event.respondWith(
		(async function () {
			const cache = await caches.open(CACHE_NAME);
			console.log('NETWORKFIRST: ', event.request.url);
			let resp;
			try {
				resp = await fetch(event.request);
			} catch (e) {
				console.log('FETCH ERROR: ', e);
				const cachedResponse = await caches.match(event.request, { ignoreSearch: true });
				if (cachedResponse) {
					return cachedResponse;
				} else {
					if (event.request.mode === 'navigate') return cache.match('/offline');
					else return resp;
				}
			}
			if (resp.ok) event.waitUntil(cache.put(event.request, resp.clone()));
			return resp;
		})()
	);
}

/** @param {FetchEvent} event */
function networkOnly(event) {
	event.respondWith(async () => fetch(event.request));
}

// don't cache during development
if (prerendered.length !== 0) {
	sw.addEventListener('fetch', function (event) {
		const url = new URL(event.request.url);
		if (
			event.request.method !== 'GET' ||
			url.pathname.endsWith('.js.map') ||
			(sw.location.hostname === url.hostname && url.pathname.startsWith('/api')) || // webpush
			(url.hostname.endsWith('.supabase.co') && url.pathname.startsWith('/auth/')) // supabase auth
			// todo: pvt
		) {
			return; // let the browser do its default thing
		} else if (
			url.hostname === 'graphql.contentful.com' ||
			url.hostname.endsWith('.supabase.co') ||
			url.pathname === '/_app/version.json'
		) {
			networkFirst(event);
		} else if (
			url.pathname.startsWith('/_app/immutable/') || // assets are immutable (versioned in url)
			// any other assets served as part of the app bundle, all need to be the same version
			// having misversioned assets will cause pages to crash
			// these will be updated in the bulk precache when the app is updated
			url.hostname === sw.location.hostname
		) {
			cacheFirst(event, false);
		} else {
			// any other random assets that the app loads are cachable
			cacheFirst(event, true); // stale while etag revalidate
		}
	});
}

const notificationOptions = { icon: '/favicon.ico', badge: '/4h-96x96.png' };

sw.addEventListener('push', (e) => {
	e.waitUntil(
		(async () => {
			console.log('Push received', e);
			const pushData = e.data.json();
			console.log('Push data', pushData);
			if (pushData.type === 'notification') {
				await sw.registration.showNotification(pushData.data.title, {
					body: pushData.data.body,
					...notificationOptions,
					...pushData.data.options,
				});
			} else if (pushData.type === 'test') {
				console.log('testing push');
				// not supported well on ios :/
				// const broadcast = new BroadcastChannel('push-test');
				// broadcast.postMessage(pushData);
				// broadcast.close(); // allow channel to be garbage collected
				const clients = await sw.clients.matchAll({ includeUncontrolled: true, type: 'window' });
				for (const client of clients) {
					client.postMessage({ id: pushData.id, type: 'PUSH_TEST' });
				}

				await sw.registration.showNotification('Your notifications are working!', {
					body: 'The latest fair news will arrive here.',
					silent: true,
					tag: 'push-test',
					actions: [
						{
							action: '/settings#notifications',
							title: 'Notification settings',
						},
					],
					...notificationOptions,
				});
			}
		})()
	);
});

sw.addEventListener('notificationclick', (event) => {
	console.log('On notification click: ', event.notification.tag);
	event.notification.close();
	if (event.action) {
		return sw.clients.openWindow(event.action);
	} else {
		event.waitUntil(
			sw.clients
				.matchAll({
					type: 'window',
				})
				.then((clientList) => {
					for (const client of clientList) {
						console.log(client);
						if (new URL(client.url).pathname === '/' && 'focus' in client) return client.focus();
					}
					return sw.clients.openWindow('/');
				})
		);
	}
});

sw.addEventListener('pushsubscriptionchange', (event) => {
	event.waitUntil(async () => {
		/** @type {PushSubscription|null} */
		let newSubscription = event.newSubscription,
			/** @type {PushSubscription|null} */
			oldSubscription = event.oldSubscription;

		if (!newSubscription) {
			// try resubscribing
			newSubscription = await sw.registration.pushManager.subscribe({
				userVisibleOnly: true,
				applicationServerKey:
					'BEVhADYtzjjK1odWzYgXNZmiO90ugEBch6S8taqPnCL3Fbdpc1NNPSsJa-HJDXM57FrvfJc7TBMqWuB51mdkT7k',
				...oldSubscription?.options,
			});
		}

		const res = await fetch(`${__WEBPUSH_API_PREFIX__}/api/webpush/resubscribe`, {
			method: 'POST',
			body: JSON.stringify({ subscription: newSubscription, oldSubscription }),
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		});
		console.log('resubscribe response', res);
	});
});
