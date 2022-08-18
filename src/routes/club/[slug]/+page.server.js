import { getClubs } from 'logic/contentful.js';

export async function load() {
	const resp = await getClubs();
	return { clubs: resp };
}
