import { getSponsors } from 'logic/contentful';

export async function load() {
	const resp = await getSponsors();
	return { sponsors: resp };
}

export const trailingSlash = 'never';
export const prerender = true;
