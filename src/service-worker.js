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

sw.addEventListener('install', function (event) {
	// sw.skipWaiting();
	console.log('Service worker installing');
	event.waitUntil(
		(async () => {
			const cache = await caches.open(CACHE_NAME);

			console.log('PRECACHE SIZE', PRECACHE.length);

			let toCache = PRECACHE,
				toUncache = [];
			const existingKeys = await cache.keys();

			for (const req of existingKeys) {
				const url = new URL(req.url),
					immutable = url.pathname.startsWith('/_app/immutable');
				if (immutable && toCache.includes(url.pathname)) {
					// immutable files are hashed, we can skip caching them again
					toCache.splice(toCache.indexOf(url.pathname), 1);
				} else if (url.origin === location.origin && !toCache.includes(url.pathname)) {
					// we can remove them from the cache if they are no longer in the precache
					await cache.delete(req);
					toUncache.push(req.url);
				}
			}

			console.log('PRECACHE SIZE REDUCED TO', toCache.length);
			console.log('UNCACHED', toUncache.length, 'OLD FILES', toUncache);

			try {
				await cache.addAll(toCache);
				console.log('PRECACHE COMPLETE');
			} catch (e) {
				console.log('PRECACHE FAILED: ', e);
			}

			try {
				// remove old cache from v1 of the app
				await caches.delete('offline-cache-v1');
			} catch (e) {
				console.log("didn't delete v1 cache", e);
			}
		})()
	);
});

sw.addEventListener('message', (event) => {
	if (event?.data?.type === 'SKIP_WAITING') {
		sw.skipWaiting(); // install new sw (update caches), then activate (reload old versions)
	}
});

sw.addEventListener('activate', async () => {
	// ensure we are never running any old versions
	// after we've taken over, iterate over all the current clients (windows)
	const tabs = await sw.clients.matchAll({ type: 'window' });
	tabs.forEach((tab) => {
		// and refresh each one of them
		tab.navigate(tab.url);
	});
});

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
								await cache.add(event.request);
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
					// fixme: this is broken as sveltekit's routing doesn't trigger this
					// we could hook into the router and force the navigation if we wanted
					// https://github.com/sveltejs/kit/issues/2570 for some reference
					if (event.request.mode === 'navigate') return cache.match('/offline');
					else return resp;
				}
				event.waitUntil(cache.put(event.request, resp.clone()));
				return resp;
			}
		})()
	);
}

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
			event.waitUntil(cache.put(event.request, resp.clone()));
			return resp;
		})()
	);
}

function networkOnly(event) {
	event.respondWith(async () => fetch(event.request));
}

// don't cache during development
if (prerendered.length !== 0) {
	sw.addEventListener('fetch', function (event) {
		const url = new URL(event.request.url);
		if (
			event.request.method !== 'GET' ||
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
		} else if (url.pathname.startsWith('/_app/immutable/')) {
			cacheFirst(event, false); // no revalidate, as these assets are immutable (versioned in url)
		} else {
			cacheFirst(event, true); // stale while etag revalidate
		}
	});
}

const notificationOptions = { icon: '/favicon.ico', badge: '/4h-96x96.png' };

sw.addEventListener('push', (e) => {
	console.log('Push received', e);
	const pushData = e.data.json();
	console.log('Push data', pushData);
	if (pushData.type === 'notification') {
		e.waitUntil(
			sw.registration.showNotification(pushData.data.title, {
				body: pushData.data.body,
				...notificationOptions,
				...pushData.data.options,
			})
		);
	} else if (pushData.type === 'test') {
		const broadcast = new BroadcastChannel('push-test');
		console.log('testing push');
		broadcast.postMessage(pushData);
		broadcast.close(); // allow channel to be garbage collected
		e.waitUntil(
			sw.registration.showNotification('Your notifications are working!', {
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
			})
		);
	}
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
