import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

export const menuOpen = writable(false);

export const isOnline = writable(isBrowser ? navigator.onLine : true);
if (isBrowser) {
	window.addEventListener('online', () => isOnline.set(true));
	window.addEventListener('offline', () => isOnline.set(false));
	isOnline.subscribe((state) => {
		if (state) document.body.style.removeProperty('--status-bar');
		else document.body.style.setProperty('--status-bar', '#888');
		document
			.querySelector('meta[name="theme-color"]')
			.setAttribute('content', getComputedStyle(document.body).getPropertyValue('--status-bar'));
	});
}
