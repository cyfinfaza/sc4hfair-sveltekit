import { createClient } from '@supabase/supabase-js';
import { writable } from 'svelte/store';

let client = null;

export const session = writable();
export const interestsSlugs = writable();

export async function initSupabaseClient() {
	if (!client) {
		client = await createClient(
			'https://gahyqgeshbvyajzukktr.supabase.co',
			'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMjIzMjcyMywiZXhwIjoxOTM3ODA4NzIzfQ.qeJRUDnHvCdSTo6LQUCbwe6XQFSLsi2l4_3oD9189u8'
		);
		window.supabase = client;
		let sess = await client.auth.session();
		console.log(sess);
		session.update((_) => sess);
		refresh();
		client.auth.onAuthStateChange(async (event, sess) => {
			session.update((_) => sess);
			refresh();
		});
	}
	return client;
}

export async function refresh() {
	const sess = await client.auth.session();
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
		interestsSlugs.update((_) => results.map((result) => result.interest_slug));
	} else {
		interestsSlugs.update((_) => []);
	}
}

export async function login(provider, redirect = '/interests') {
	// const { user, session, error } = await client.auth.signIn(
	await client.auth.signIn(
		{
			provider: provider,
		},
		{
			redirectTo: window.location.origin + redirect,
		}
	);
}

export function logout() {
	client.auth.signOut();
	// window.location.reload()
}

export async function verifySession(action) {
	let sess = await client.auth.session();
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
		owner: client.auth.session().user.id,
	});
	if (error) console.error(error);
	refresh();
	// setTimeout(() => {
	// 	refresh()
	// }, 500)
}
