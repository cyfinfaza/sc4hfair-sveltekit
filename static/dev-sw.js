/*
await navigator.serviceWorker.register('/dev-sw.js', { scope: '/' });
*/

self.addEventListener('install', () => {
	self.skipWaiting();
	console.log('Service worker installed');
});

// also update in service-worker.js
self.addEventListener('push', (e) => {
	console.log('Push received', e);
	const pushData = e.data.json();
	console.log('Push data', pushData);
	if (pushData.type === 'notification') {
		e.waitUntil(
			self.registration.showNotification(pushData.data.title, {
				body: pushData.data.body,
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
