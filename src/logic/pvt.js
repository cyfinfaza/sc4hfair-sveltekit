import { checkIsStandalone } from 'logic/platform';

export function pvtUpdate() {
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
