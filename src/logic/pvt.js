import { checkIsStandalone } from 'logic/platform';

export function pvtUpdate() {
	let reqInit = {
		method: 'POST',
		body: JSON.stringify({
			url: window.location.href,
			meta: {
				standalone: checkIsStandalone(),
				sh_2023_code: localStorage.getItem('sh_2023_code') || undefined,
			},
		}),
		credentials: 'include',
		type: 'application/json',
	};
	fetch('/api/pvt', reqInit).then((response) =>
		response.text().then((status) => {
			console.log('track:', status);
			if (status === 'unconfirmed') {
				fetch('/api/pvt', reqInit);
			}
		})
	);
}
