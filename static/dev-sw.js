self.addEventListener('install', () => {
	self.skipWaiting();
	console.log('Service worker installed');
});

self.addEventListener('push', (e) => {
	console.log('Push received', e);
	const pushData = e.data.json();
	console.log('Push data', pushData);
	if (pushData.type === 'notification') {
		e.waitUntil(self.registration.showNotification(pushData.title, pushData.options));
	}
});
