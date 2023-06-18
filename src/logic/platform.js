import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export function getPlatform() {
	if (typeof window === 'undefined') return 'other';

	var userAgent = navigator.userAgent || navigator.vendor;

	if (/android/i.test(userAgent)) {
		if (/wv|FBAV/.test(userAgent)) return 'android-unsupported';

		return 'android';
	}

	if (/iPad|iPhone|iPod|iOS/.test(userAgent) || navigator.vendor === 'Apple Computer, Inc.') {
		if (/CriOS|FxiOS|EdgiOS|FBIOS/.test(userAgent)) return 'ios-unsupported';

		return 'ios';
	}

	// if (/chrome/i.test(userAgent)) return 'desktop'

	return 'other';
}

const standaloneModes = ['standalone', 'fullscreen', 'minimal-ui'];
/** @returns {boolean} */
const checkIsStandalone = () =>
	browser &&
	(window.navigator.standalone ||
		standaloneModes.some((mode) => window.matchMedia(`(display-mode: ${mode})`).matches));

export const isStandalone = writable(checkIsStandalone());

// subscribe to browser updates
if (browser)
	standaloneModes.forEach((mode) => {
		window.matchMedia(`(display-mode: ${mode})`).addEventListener('change', () => {
			isStandalone.set(checkIsStandalone());
		});
	});
