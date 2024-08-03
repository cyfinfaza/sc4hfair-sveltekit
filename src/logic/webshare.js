import { browser } from '$app/environment';
import { get, writable } from 'svelte/store';
import { kioskMode } from './stores';

export const canWebShare = writable(false);

export function share(title, url) {
	if (navigator.share) {
		navigator.share({ title, url }).catch(() => console.error('Share failed'));
	} else {
		console.error('navigator.share unavailable');
	}
}
