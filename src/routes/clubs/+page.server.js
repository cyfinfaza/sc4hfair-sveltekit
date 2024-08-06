import { getClubs } from 'logic/contentful.js';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
	const clubs = await getClubs();
	return { clubs };
}
