export async function queryContentful(query) {
	const res = await fetch(
		'https://graphql.contentful.com/content/v1/spaces/e34g9w63217k/?query=' +
			encodeURIComponent(query),
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${atob(
					'VFJsQ28xQmxUbXB3eUtJT0hKMDhYMmxZQWFOTmxjZUY0MTVLTW1La01Gaw=='
				)}`,
			},
		}
	);
	if (!res.ok) throw new Error(await res.text());
	return (await res.json()).data;
}

let clubs = [];
const clubQuery = `{
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
			}
	}
}`;
export async function getClubs() {
	if (clubs.length === 0) {
		clubs = (await queryContentful(clubQuery)).clubCollection.items;
	}
	return clubs;
}

let sponsors = [];
const sponsorQuery = `{
	sponsorSpotCollection {
		items {
			heading
			image {
				url
			}
			description
			link
			tier
		}
	}
}`;
export async function getSponsors() {
	if (sponsors.length === 0) {
		sponsors = (await queryContentful(sponsorQuery)).sponsorSpotCollection.items;
	}
	return sponsors;
}
