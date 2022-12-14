export function requestNotificationPermission() {
	return new Promise((resolve, reject) => {
		if (!('Notification' in window)) {
			reject(new Error('Notifications are not supported'));
		}
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
		throw new Error('Notification permission not granted');
	}
	const registration = await Promise.race([
		navigator.serviceWorker.ready,
		new Promise((_, reject) =>
			setTimeout(() => reject('No service worker detected within 30s'), 30000)
		),
	]);
	await registration.pushManager.subscribe({
		userVisibleOnly: true,
		applicationServerKey:
			'BEVhADYtzjjK1odWzYgXNZmiO90ugEBch6S8taqPnCL3Fbdpc1NNPSsJa-HJDXM57FrvfJc7TBMqWuB51mdkT7k',
	});
	const subscription = await registration.pushManager.getSubscription();
	console.log(subscription);
	return subscription;
}

export async function checkNotificationStatus() {
	if (!('Notification' in window)) {
		throw new Error('Notifications are not supported');
	}
	if (Notification.permission !== 'granted') {
		console.warn('Notifications unavailable because permission is not granted.');
		return false;
	}
	if ((await subscribe(true)).registered === false) {
		console.warn('Notifications unavailable because subscription does not exist.');
		return false;
	}
	return true;
}

/**
 * @typedef WebpushApiResponse
 * @type {object}
 * @property {'success' | 'error'} type
 * @property {string} [message]
 * @property {boolean} [already_exists] - if the subscription was previously registered
 * @property {boolean} [registered] - if the subscripion is registered after any actions complete
 * @property {string} [test_id] - uuid id sent back to the client to test webpush
 */

export async function subscribe(dry = false) {
	// get subscription
	const subscription = await getSubscription();
	if (!subscription) throw new Error('Service worker subscription not found');

	if (!dry) {
		// prepare to get a test message
		var broadcast = new BroadcastChannel('push-test');
		var resolveTestId,
			rejectTestId,
			testId = new Promise((resolve, reject) => {
				resolveTestId = resolve;
				rejectTestId = reject;
			});
		broadcast.onmessage = (e) => {
			if (e.data.id) resolveTestId(e.data.id);
		};
	}

	// send subscription to server
	const sub = await fetch('https://v2.sc4hfair.app/api/webpush/subscribe' + (dry ? '?dry' : ''), {
		method: 'POST',
		body: JSON.stringify({ subscription }),
		headers: {
			'Content-Type': 'application/json',
		},
		credentials: 'include',
	});
	/** @type {WebpushApiResponse} */
	const data = await sub.json();
	console.log(data);
	if (!sub.ok || data.type !== 'success') throw data;

	if (!dry) {
		// wait for test message before giving up
		let testIdMatched = false;
		await Promise.race([testId, new Promise((_, reject) => setTimeout(reject, 5000))])
			.then((id) => (testIdMatched = id === data.test_id))
			.catch(() => {
				throw new Error('Test push not received within 5s');
			});
		broadcast.close(); // allow channel to be garbage collected

		console.log('test id matched:', testIdMatched);
		// @todo: reply to server if matched and then have server add to db
	}

	return data;
}

export async function unsubscribe() {
	// get subscription
	const subscription = await getSubscription();
	if (!subscription) throw new Error('No subscription');

	// send subscription to server
	const sub = await fetch('https://v2.sc4hfair.app/api/webpush/unsubscribe', {
		method: 'POST',
		body: JSON.stringify({ subscription }),
		headers: {
			'Content-Type': 'application/json',
		},
		credentials: 'include',
	});
	/** @type {WebpushApiResponse} */
	const data = await sub.json();
	console.log(data);
	if (!sub.ok || data.type !== 'success') throw data;
	return data;
}
