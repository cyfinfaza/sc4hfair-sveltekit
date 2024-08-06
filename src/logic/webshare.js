import { writable } from 'svelte/store';

export const canWebShare = writable(false);

/**
 * @param {string} title
 * @param {string} url
 */
export function share(title, url) {
	if (navigator.share) {
		navigator.share({ title, url }).catch(() => console.error('Share failed'));
	} else {
		console.error('navigator.share unavailable');
	}
}
