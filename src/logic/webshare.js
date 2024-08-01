import { browser } from '$app/environment';

export const canWebShare = () => browser && navigator.share;

export function share(title, url) {
	if (navigator.share) {
		navigator.share({ title, url }).catch(() => console.error('Share failed'));
	} else {
		console.error('navigator.share unavailable');
	}
}
