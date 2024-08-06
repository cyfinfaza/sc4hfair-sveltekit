import { browser } from '$app/environment';
import { createClient } from '@supabase/supabase-js';
import { get, writable } from 'svelte/store';
import { isOnline } from './stores';
import { STORAGE_KEY } from '@supabase/auth-js/src/lib/constants';

/** @type {import('@supabase/supabase-js').SupabaseClient | null} */
let _client = null;

/** @type {import('svelte/store').Writable<import('@supabase/auth-js').Session | null>} */
export const session = writable();
/** @type {import('svelte/store').Writable<string[]>} */
export const interestsSlugs = writable();

export async function initSupabaseClient() {
	if (!_client) {
		_client = await createClient(
			'https://gahyqgeshbvyajzukktr.supabase.co',
			'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMjIzMjcyMywiZXhwIjoxOTM3ODA4NzIzfQ.qeJRUDnHvCdSTo6LQUCbwe6XQFSLsi2l4_3oD9189u8'
		);
		// @ts-expect-error
		window.supabase = _client;
		const sess = (await _client.auth.getSession())?.data?.session;
		console.log(sess);
		session.set(sess);
		refresh();
		_client.auth.onAuthStateChange(async (event, sess) => {
			session.set(sess);
			refresh();
		});
		isOnline.subscribe((online) => {
			if (online) refresh();
		});
	}
	return _client;
}

export async function refresh() {
	let client = await initSupabaseClient();
	const sess = (await client.auth.getSession())?.data?.session;
	session.set(sess);
	console.log(sess);
	if (sess) {
		try {
			let intent = localStorage.getItem('cim_intent');
			if (intent) {
				localStorage.removeItem('cim_intent');
				/** @type {CIMAction} */
				let intentData = JSON.parse(intent);
				if (intentData.action === 'add') await addInterest(intentData.slug);
				else if (intentData.action === 'remove') await removeInterest(intentData.slug);
			}
		} catch (error) {
			console.error(error);
		}
		let { data: results, error } = await client.from('interests').select('*');
		if (error) console.error(error);
		console.log(results);
		interestsSlugs.set(results?.map((result) => result.interest_slug) || []);
	} else {
		await removeCachedData();
	}
}

/** @param {import('@supabase/auth-js').Provider} provider */
export async function login(provider, redirect = '/interests') {
	// const { data, error } =
	await (
		await initSupabaseClient()
	).auth.signInWithOAuth({
		provider: provider,
		options: {
			redirectTo: globalThis.location.origin + redirect,
		},
	});
}

/** When logging out, we don't want to keep stale login/user data */
async function removeCachedData() {
	interestsSlugs.set([]);
	if (browser) {
		// delete any cached supabase responses
		const keys = await globalThis.caches.keys();
		await Promise.all(
			keys.map(async (key) => {
				const cache = await globalThis.caches.open(key);
				await Promise.all(
					(await cache.keys()).map(async (req) => {
						if (req.url.includes('.supabase.co/')) await cache.delete(req);
					})
				);
			})
		);
	}
}

export async function logout() {
	let client = await initSupabaseClient();
	if (!get(isOnline)) {
		// remove the session token from the client and call it day
		// the session token is still valid on the server but it's probably fine enough for our uses
		localStorage.removeItem(STORAGE_KEY);
		const sess = (await client.auth.getSession()).data.session;
		if (sess !== null) throw new Error('Failed to clear Supabase session');
		session.set(sess);
	} else {
		await client.auth.signOut();
	}
	await removeCachedData();
	// window.location.reload()
}

/**
 * @typedef {object} CIMAction
 * @property {'add' | 'remove'} action
 * @property {string} slug
 */

/** @param {CIMAction} action */
export async function verifySession(action) {
	const sess = (await (await initSupabaseClient()).auth.getSession())?.data?.session;
	if (!sess) {
		localStorage.setItem('cim_intent', JSON.stringify(action));
		window.location.href = '/interests?reqLoginMessage=true';
		return false;
	}
	return true;
}

/** @param {string} slug */
export async function removeInterest(slug) {
	if (!verifySession({ action: 'remove', slug: slug })) return;
	let { error } = await (await initSupabaseClient())
		.from('interests')
		.delete()
		.match({ interest_slug: slug });
	if (error) console.error(error);
	refresh();
}

/** @param {string} slug */
export async function addInterest(slug) {
	if (!verifySession({ action: 'add', slug: slug })) return;
	let { error } = await (await initSupabaseClient()).from('interests').insert({
		interest_slug: slug,
		owner: get(session)?.user.id,
	});
	if (error) console.error(error);
	refresh();
}
