import { browser } from '$app/environment';
import { createClient } from '@supabase/supabase-js';
import { get, writable } from 'svelte/store';
import { isOnline } from './stores';

/** @type {import('@supabase/supabase-js').SupabaseClient} */
let client = null;

/** @type {import('svelte/store').Writable<import('@supabase/gotrue-js').Session|null>} */
export const session = writable();
export const interestsSlugs = writable();

export async function initSupabaseClient() {
	if (!client) {
		client = await createClient(
			'https://gahyqgeshbvyajzukktr.supabase.co',
			'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMjIzMjcyMywiZXhwIjoxOTM3ODA4NzIzfQ.qeJRUDnHvCdSTo6LQUCbwe6XQFSLsi2l4_3oD9189u8'
		);
		window.supabase = client;
		const sess = (await client.auth.getSession())?.data?.session;
		console.log(sess);
		session.update((_) => sess);
		refresh();
		client.auth.onAuthStateChange(async (event, sess) => {
			session.update((_) => sess);
			refresh();
		});
		isOnline.subscribe((online) => {
			if (online) refresh();
		});
	}
	return client;
}

export async function refresh() {
	const sess = (await client.auth.getSession())?.data?.session;
	session.update((_) => sess);
	console.log(sess);
	if (sess) {
		try {
			let intent = localStorage.getItem('cim_intent');
			if (intent) {
				localStorage.removeItem('cim_intent');
				intent = JSON.parse(intent);
				if (intent.action === 'add') await addInterest(intent.slug);
				if (intent.action === 'remove') await removeInterest(intent.slug);
			}
		} catch (error) {
			console.error(error);
		}
		let { data: results, error } = await client.from('interests').select('*');
		if (error) console.error(error);
		console.log(results);
		interestsSlugs.update(() => results.map((result) => result.interest_slug));
	} else {
		await removeCachedData();
	}
}

export async function login(provider, redirect = '/interests') {
	// const { data, error } =
	await client.auth.signInWithOAuth({
		provider: provider,
		options: {
			redirectTo: globalThis.location.origin + redirect,
		},
	});
}

/** when logging out, we don't want to keep stale login/user data */
async function removeCachedData() {
	interestsSlugs.update(() => []);
	if (browser) {
		// delete any cached supabase responses
		const keys = await globalThis.caches.keys();
		await Promise.all(
			keys.map(async (key) => {
				const cache = await globalThis.caches.open(key);
				await Promise.all(
					(
						await cache.keys()
					).map(async (req) => {
						if (req.url.includes('.supabase.co/')) await cache.delete(req);
					})
				);
			})
		);
	}
}

export async function logout() {
	if (!get(isOnline)) {
		// remove the session token from the client and call it day
		// the session token is still valid on the server but it's probably fine enough for our uses
		localStorage.removeItem(client.auth.storageKey);
		const sess = (await client.auth.getSession()).data.session;
		if (sess !== null) throw new Error('Failed to clear Supabase session');
		session.update((_) => sess);
	} else {
		await client.auth.signOut();
	}
	await removeCachedData();
	// window.location.reload()
}

export async function verifySession(action) {
	const sess = (await client.auth.getSession())?.data?.session;
	if (!sess) {
		localStorage.setItem('cim_intent', JSON.stringify(action));
		window.location = '/interests?reqLoginMessage=true';
		return false;
	}
	return true;
}

export async function removeInterest(slug) {
	if (!verifySession({ action: 'remove', slug: slug })) return;
	let { error } = await client.from('interests').delete().match({ interest_slug: slug });
	if (error) console.error(error);
	refresh();
}

export async function addInterest(slug) {
	if (!verifySession({ action: 'add', slug: slug })) return;
	let { error } = await client.from('interests').insert({
		interest_slug: slug,
		owner: get(session).user.id,
	});
	if (error) console.error(error);
	refresh();
	// setTimeout(() => {
	// 	refresh()
	// }, 500)
}
