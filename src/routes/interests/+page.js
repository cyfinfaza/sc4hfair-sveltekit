import { queryContentful } from 'logic/contentful.js';

const query = `{
	clubCollection {
		items {
			slug
				name
				meetingLocation
				clubWebsite
				description
				grades
				meetingWhen
				listingWebsite
				tent
		}
	}
}`;

export async function load({ fetch }) {
	const resp = await queryContentful(fetch, query);
	return { clubs: resp.clubCollection?.items };
}
