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
	if (!subscription) throw new Error('No subscription');

	// prepare to get a test message
	const broadcast = new BroadcastChannel('push-test');
	let resolveTestId,
		rejectTestId,
		testId = new Promise((resolve, reject) => {
			resolveTestId = resolve;
			rejectTestId = reject;
		});
	broadcast.onmessage = (e) => {
		if (e.data.id) resolveTestId(e.data.id);
	};

	// send subscription to server
	const sub = await fetch('https://v2.sc4hfair.app/api/webpush/subscribe/' + (dry ? '?dry' : ''), {
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

	// wait for test message before giving up
	let testIdMatched = false;
	await Promise.race([testId, new Promise((_, reject) => setTimeout(reject, 5000))])
		.then((id) => (testIdMatched = id === data.test_id))
		.catch(() => console.error("didn' get test message"));
	broadcast.close(); // allow channel to be garbage collected

	console.log('test id matched:', testIdMatched);
	// @todo: reply to server if matched and then have server add to db

	return data;
}

export async function unsubscribe() {
	// get subscription
	const subscription = await getSubscription();
	if (!subscription) throw new Error('No subscription');

	// send subscription to server
	const sub = await fetch('https://v2.sc4hfair.app/api/webpush/unsubscribe/', {
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
