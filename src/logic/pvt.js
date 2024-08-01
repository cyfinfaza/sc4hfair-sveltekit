import { SCAVENGER_HUNT_CODE } from 'logic/constants';
import { checkIsStandalone } from 'logic/platform';

export function pvtUpdate({ href = window.location.href, referrer = undefined }) {
	let reqInit = {
		method: 'POST',
		body: JSON.stringify({
			url: href,
			meta: {
				standalone: checkIsStandalone(),
				[SCAVENGER_HUNT_CODE]: localStorage.getItem(SCAVENGER_HUNT_CODE) || undefined,
				referrer: referrer || undefined,
				kiosk: localStorage.getItem('kiosk') === '1' || undefined,
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
