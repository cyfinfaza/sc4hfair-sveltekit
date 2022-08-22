import { build, files, prerendered, version } from '$service-worker';

const CACHE_NAME = 'offline-cache-v1';
const PRECACHE = ['_app/version.json', ...build, ...files, ...prerendered];

console.log('precache: ', PRECACHE);
console.log('version: ', version);

self.addEventListener('install', function (event) {
	self.skipWaiting();
	console.log('Service worker installing');
	event.waitUntil(
		(async (_) => {
			try {
				const cache = await caches.open(CACHE_NAME);
				await cache.addAll(PRECACHE);
				console.log('PRECACHE COMPLETE');
			} catch (e) {
				console.log('PRECACHE FAILED: ', e);
			}
		})()
	);
});

function staleWhileEtagRevalidate(event) {
	event.respondWith(
		(async function () {
			const cache = await caches.open(CACHE_NAME);
			const cachedResponse = await cache.match(event.request);
			console.log(cachedResponse);
			if (cachedResponse) {
				const cacheEtag = cachedResponse.headers.get('etag');
				console.log('CACHED: ', cachedResponse.url, cacheEtag);
				event.waitUntil(
					(async (_) => {
						const headRequest = await fetch(event.request.url, { method: 'HEAD' });
						const headEtag = headRequest.headers.get('etag');
						console.log('REVALIDATE HEAD CHECK: ', cachedResponse.url, cacheEtag);
						if (headEtag && cacheEtag !== headEtag) {
							console.log('REVALIDATING: ', cachedResponse.url);
							await cache.delete(event.request);
							await cache.add(event.request);
						}
					})()
				);
				return cachedResponse;
			} else {
				console.log('CACHE MISS: ', event.request.url);
				let resp;
				try {
					resp = await fetch(event.request);
				} catch (e) {
					console.log('FETCH ERROR: ', e);
					return cache.match('/offline');
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
				const cachedResponse = await caches.match(event.request);
				if (cachedResponse) {
					return cachedResponse;
				} else {
					return cache.match('/offline');
				}
			}
			event.waitUntil(cache.put(event.request, resp.clone()));
			return resp;
		})()
	);
}

self.addEventListener('fetch', function (event) {
	if (new URL(event.request.url).hostname === 'graphql.contentful.com') {
		networkFirst(event); // @todo: expiration cache
	} else {
		staleWhileEtagRevalidate(event);
	}
});

self.addEventListener('push', (e) => {
	console.log('Push received', e);
	const pushData = e.data.json();
	console.log('Push data', pushData);
	if (pushData.type === 'notification') {
		e.waitUntil(
			self.registration.showNotification(pushData.data.title, {
				body: pushData.data.body,
				icon: '/favicon.ico',
				badge: '/4h-96x96.png',
				...pushData.data.options,
			})
		);
	} else if (pushData.type === 'test') {
		const broadcast = new BroadcastChannel('push-test');
		console.log('testing push');
		broadcast.postMessage(pushData);
		broadcast.close(); // allow channel to be garbage collected
	}
});

self.addEventListener('notificationclick', (event) => {
	console.log('On notification click: ', event.notification.tag);
	event.notification.close();
	event.waitUntil(
		clients
			.matchAll({
				type: 'window',
			})
			.then((clientList) => {
				for (const client of clientList) {
					console.log(client);
					if (new URL(client.url).pathname === '/' && 'focus' in client) return client.focus();
				}
				if (clients.openWindow) return clients.openWindow('/');
			})
	);
});
