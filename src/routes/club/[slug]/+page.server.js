import { error } from '@sveltejs/kit';
import { getClubs } from 'logic/contentful.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	const clubs = await getClubs();
	// it is important that we only return the club that we want to render
	// so each page will NOT have a copy of the whole club list, only the one it needs
	const club = clubs.find((club) => club.slug === params.slug);

	if (!club) {
		return error(404);
	}

	return { club };
}
