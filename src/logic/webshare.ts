import { writable } from 'svelte/store';

export const canWebShare = writable(false);

export function share(title: string, url: string) {
	if (navigator.share) {
		navigator.share({ title, url }).catch(() => console.error('Share failed'));
	} else {
		console.error('navigator.share unavailable');
	}
}
