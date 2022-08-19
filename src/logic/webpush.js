export function requestNotificationPermission() {
	return new Promise((resolve, reject) => {
		window.Notification.requestPermission(function (status) {
			console.log('Notification permission status: ', status);
			resolve(status);
		});
	});
}

export async function getSubscription() {
	// debugger;
	const permission = await requestNotificationPermission();
	if (permission !== 'granted') {
		console.error('Notification permission not granted', permission);
		return;
	}
	const registration = await navigator.serviceWorker.ready;

	await registration.pushManager.subscribe({
		userVisibleOnly: true,
		applicationServerKey:
			'BEVhADYtzjjK1odWzYgXNZmiO90ugEBch6S8taqPnCL3Fbdpc1NNPSsJa-HJDXM57FrvfJc7TBMqWuB51mdkT7k',
	});
	const subscription = await registration.pushManager.getSubscription();
	console.log(subscription);
	return subscription;
}
