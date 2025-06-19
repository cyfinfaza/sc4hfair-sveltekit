import { browser } from '$app/environment';
import { get, writable, type Writable } from 'svelte/store';
import { session, type Session } from './auth';
import { isOnline } from './stores.svelte';
import { goto } from '$app/navigation';

export const interestsSlugs: Writable<string[]> = writable([]);

interface CIMAction {
	action: 'add' | 'remove';
	slug: string;
}

export async function refresh(sess: Session | null) {
	if (sess) {
		try {
			let intent = localStorage.getItem('cim_intent');
			if (intent) {
				localStorage.removeItem('cim_intent');
				let intentData: CIMAction = JSON.parse(intent);
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

export async function verifySession(action: CIMAction) {
	const sess = get(session);
	if (!sess) {
		localStorage.setItem('cim_intent', JSON.stringify(action));
		goto('/interests?reqLoginMessage=true');
		return false;
	}
	return true;
}

export async function removeInterest(slug: string) {
	if (!verifySession({ action: 'remove', slug: slug })) return;

	const res = await fetch(`/api/interests/${slug}`, {
		method: 'DELETE',
		credentials: 'include',
	});

	if (res.ok) interestsSlugs.update((slugs) => slugs.filter((s) => s !== slug));
}

export async function addInterest(slug: string) {
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
