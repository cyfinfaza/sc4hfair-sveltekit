import { writable } from 'svelte/store';

export interface Session {
	sub: string;
	email: string;
	exp: number;
}

type SessionProvider = 'google';

/**
 * Parses the session token from the cookie and returns the session object. Do not use for secure
 * reasons, as it is not signature verified.
 */
function getSession(): Session | null {
	try {
		const payload =
			'document' in globalThis &&
			document.cookie
				.split(';')
				.find((cookie) => cookie.trim().startsWith('session_token='))
				?.split('=')[1]
				?.split('.')[1];
		return (payload && JSON.parse(window.atob(payload))) || null;
	} catch (e) {
		return null;
	}
}

// todo: implement loading state
export const session = writable(getSession());

export function login(provider: SessionProvider, redirect = globalThis?.location.pathname) {
	location.href = `/api/auth/${provider}-init?redirect=${encodeURIComponent(globalThis.location.origin + redirect)}`;
}

/** When logging out, we don't want to keep stale login/user data */
async function removeCachedData() {
	// todo: port to new system?
	// if (browser) {
	// 	// delete any cached supabase responses
	// 	const keys = await globalThis.caches.keys();
	// 	await Promise.all(
	// 		keys.map(async (key) => {
	// 			const cache = await globalThis.caches.open(key);
	// 			await Promise.all(
	// 				(await cache.keys()).map(async (req) => {
	// 					if (req.url.includes('.supabase.co/')) await cache.delete(req);
	// 				})
	// 			);
	// 		})
	// 	);
	// }
}

export function logout() {
	// fetch('/api/auth/logout', {
	// 	method: 'POST',
	// });
	document.cookie = 'session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
	session.set(null);
	removeCachedData();
}

export async function getProfile() {
	const { profile } = await (
		await fetch('/api/profile', {
			credentials: 'include',
		})
	).json();
	return profile;
}
