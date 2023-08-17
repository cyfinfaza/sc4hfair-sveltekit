import { checkIsStandalone } from 'logic/platform';

/** @type {()=>{}} */
export let pushPoprxUpdate;

export function startPoprx(addr) {
	let txid = window.localStorage.getItem('poprx-txid');
	if (!txid) {
		txid = Math.floor(Math.random() * 900000) + 100000;
		window.localStorage.setItem('poprx-txid', txid);
	}
	const client = new WebSocket(addr);
	client.onmessage = function (event) {
		const data = JSON.parse(event.data);
		console.log('poprx:', data);
	};
	client.onopen = function (event) {
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
						type: 'pathUpdate',
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

export function pvtUpdate() {
	console.log(pushPoprxUpdate);
	pushPoprxUpdate?.();
	let requestBody = JSON.stringify({
		url: window.location.href,
		meta: {
			standalone: checkIsStandalone(),
			sh_2023_code: localStorage.getItem('sh_2023_code') || undefined,
		},
	});
	fetch('/api/pvt', {
		method: 'POST',
		body: requestBody,
		credentials: 'include',
		type: 'application/json',
	}).then((response) =>
		response.text().then((status) => {
			console.log('track:', status);
			if (status === 'unconfirmed') {
				fetch('/api/pvt', {
					method: 'POST',
					body: requestBody,
					credentials: 'include',
					type: 'application/json',
				});
			}
		})
	);
}
