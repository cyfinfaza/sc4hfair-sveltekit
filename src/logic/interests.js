import { browser } from '$app/environment';
import { get, writable } from 'svelte/store';
import { session } from './auth';
import { isOnline } from './stores';
import { goto } from '$app/navigation';

/** @type {import('svelte/store').Writable<string[]>} */
export const interestsSlugs = writable([]);

/** @param {import('./auth').Session?} sess */
export async function refresh(sess) {
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

		const res = await fetch('/api/interests', {
			credentials: 'include',
		});
		if (res.ok) {
			const { interests } = await res.json();
			interestsSlugs.set(interests);
		} else {
			console.error('Failed to fetch interests:', res.statusText);
			interestsSlugs.set([]);
		}
	} else {
		interestsSlugs.set([]);
	}
}

let initialized = false;
export function initInterests() {
	if (!browser || initialized) return;

	session.subscribe(refresh);
	isOnline.subscribe((online) => {
		if (online && initialized) refresh(get(session));
	});

	initialized = true;
}

/**
 * @typedef {object} CIMAction
 * @property {'add' | 'remove'} action
 * @property {string} slug
 */

/** @param {CIMAction} action */
export async function verifySession(action) {
	const sess = get(session);
	if (!sess) {
		localStorage.setItem('cim_intent', JSON.stringify(action));
		goto('/interests?reqLoginMessage=true');
		return false;
	}
	return true;
}

/** @param {string} slug */
export async function removeInterest(slug) {
	if (!verifySession({ action: 'remove', slug: slug })) return;

	const res = await fetch(`/api/interests/${slug}`, {
		method: 'DELETE',
		credentials: 'include',
	});

	if (res.ok) interestsSlugs.update((slugs) => slugs.filter((s) => s !== slug));
}

/** @param {string} slug */
export async function addInterest(slug) {
	if (!verifySession({ action: 'add', slug: slug })) return;

	const res = await fetch(`/api/interests/${slug}`, {
		method: 'PUT',
		credentials: 'include',
	});

	if (res.ok)
		interestsSlugs.update((slugs) => {
			if (!slugs.includes(slug)) slugs.push(slug);
			return slugs;
		});
}
