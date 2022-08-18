
import { getSponsors } from 'logic/contentful.js';
export async function load({ fetch }) {
	const resp = await getSponsors(fetch);
	return { sponsors: resp };
}
