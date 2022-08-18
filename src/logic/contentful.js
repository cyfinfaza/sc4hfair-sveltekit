export async function queryContentful(fetch, query) {
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

	if (!res.ok) {
		throw new Error(await res.text());
	}
	return (await res.json()).data;
}

let clubs = [];

export async function getClubs(fetch) {
	if (clubs.length === 0) {
		clubs = (
			await queryContentful(
				fetch,
				`{
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
		}`
			)
		).clubCollection.items;
	}
	return clubs;
}

let sponsors = [];

export async function getSponsors(fetch) {
	console.log("GETTING SPONSORS")
	if (sponsors.length === 0) {
		sponsors = (
			await queryContentful(
				fetch,
				`{
			sponsorSpotCollection {
				items {
					heading
					image {
						url
					}
					description
					link
					tier
					sys {
						id
					}
				}
			}
		}`
			)
		).sponsorSpotCollection.items;
	}
	return sponsors;
}