import { getClubs } from 'logic/contentful.js';

export async function load({ fetch }) {
	const resp = await getClubs(fetch);
	return { clubs: resp };
}
