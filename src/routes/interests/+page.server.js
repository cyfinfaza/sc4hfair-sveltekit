import { getClubs } from 'logic/contentful.js';

export async function load() {
	const clubs = await getClubs();
	return { clubs };
}
