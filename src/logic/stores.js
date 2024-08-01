import { browser } from '$app/environment';
import { writable } from 'svelte/store';

export const menuOpen = writable(false);

export const isOnline = writable(browser ? navigator.onLine : true);
if (browser) {
	window.addEventListener('online', () => isOnline.set(true));
	window.addEventListener('offline', () => isOnline.set(false));
	isOnline.subscribe((state) => {
		if (state) document.body.style.removeProperty('--status-bar');
		else document.body.style.setProperty('--status-bar', '#888');
		document
			.querySelector('meta[name="theme-color"]')
			?.setAttribute('content', getComputedStyle(document.body).getPropertyValue('--status-bar'));
	});
}

export const kioskMode = writable(browser && localStorage.getItem('kiosk') === '1');
kioskMode.subscribe((state) => browser && localStorage.setItem('kiosk', state ? '1' : '0'));
