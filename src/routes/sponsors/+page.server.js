import { getSponsors } from 'logic/contentful.js';

export async function load() {
	return { sponsors: await getSponsors() };
}
