/// <reference lib="dom" />

import { SCAVENGER_HUNT_CODE } from 'logic/constants';
import { checkIsStandalone } from 'logic/platform';
import { version } from '$app/environment';

/**
 * @param {object} obj
 * @param {string | undefined} obj.href
 * @param {string | null | undefined} obj.referrer
 */
export function pvtUpdate(
	{ href = undefined, referrer = undefined } = { href: undefined, referrer: undefined }
) {
	/** @type {RequestInit} */
	let reqInit = {
		method: 'POST',
		body: JSON.stringify({
			url: href || globalThis.location.href,
			meta: {
				standalone: checkIsStandalone(),
				[SCAVENGER_HUNT_CODE]: localStorage.getItem(SCAVENGER_HUNT_CODE) || undefined,
				referrer: referrer || undefined,
				kiosk: localStorage.getItem('kiosk') === '1' || undefined,
				version,
			},
		}),
		credentials: 'include',
		headers: {
			'content-type': 'application/json',
		},
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
