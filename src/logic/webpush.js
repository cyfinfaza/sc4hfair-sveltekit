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

/**
 * Check if we can notify
 * @returns {Object} status
 * @returns {boolean} status.available if the client can subscribe
 * @returns {boolean|undefined} status.registered true if user is already registered
 * @returns {string|undefined} status.message reasoning
 */
export async function checkNotificationStatus() {
	if (!('Notification' in window)) {
		return {
			available: false,
			message: 'Notifications are not supported',
		};
	}
	// user specifically disallowed notifications
	if (Notification.permission == 'denied') {
		return {
			available: false,
			message: 'Notifications permission explicitly denied, enable it in your browser',
		};
	}
	return {
		// 'default' or 'granted' permission, doesn't hurt to ask
		available: true,
		// if we aren't granted, it doesn't matter if we already have a subscription as we can't send
		// if we try to get the subscription without permission, 💀
		registered:
			Notification.permission == 'granted'
				? (await subscribe(true)).registered // dry check, will not send a test notification
				: false,
	};
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

/** THIS WILL ASK USER FOR A SUBSCRIPTION */
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
	const sub = await fetch(`${__WEBPUSH_API_PREFIX__}/api/webpush/subscribe${dry ? '?dry' : ''}`, {
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
		let receivedId;
		await Promise.race([testId, new Promise((_, reject) => setTimeout(reject, 10000))])
			.then((id) => (receivedId = id))
			.catch(() => {});
		broadcast.close(); // allow channel to be garbage collected

		// future: reply to server if matched and then have server add to db

		if (!receivedId)
			return { ...(await unsubscribe()), message: 'Test push not received within 10s' };
		if (receivedId !== data.test_id)
			return { ...(await unsubscribe()), message: "Test push didn't match" };
	}

	return data;
}

export async function unsubscribe() {
	// get subscription
	const subscription = await getSubscription();
	if (!subscription) throw new Error('No subscription');

	// send subscription to server
	const sub = await fetch(`${__WEBPUSH_API_PREFIX__}/api/webpush/unsubscribe`, {
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
