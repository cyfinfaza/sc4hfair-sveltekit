import { SCAVENGER_HUNT_CODE } from 'logic/constants';
import { checkIsStandalone } from 'logic/platform';

export function pvtUpdate() {
	let reqInit = {
		method: 'POST',
		body: JSON.stringify({
			url: window.location.href,
			meta: {
				standalone: checkIsStandalone(),
				[SCAVENGER_HUNT_CODE]: localStorage.getItem(SCAVENGER_HUNT_CODE) || undefined,
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
