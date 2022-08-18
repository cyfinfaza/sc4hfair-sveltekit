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

export async function load() {
	const resp = await queryContentful(query);
	return { clubs: resp.clubCollection?.items };
}
