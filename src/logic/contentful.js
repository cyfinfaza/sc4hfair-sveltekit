/**
 * @template {Record<string, any>} T
 * @param {string} query
 * @returns {Promise<T>}
 */
export async function queryContentful(query) {
	const res = await fetch(
		'https://graphql.contentful.com/content/v1/spaces/e34g9w63217k/?query=' +
			encodeURIComponent(query),
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${atob('VFJsQ28xQmxUbXB3eUtJT0hKMDhYMmxZQWFOTmxjZUY0MTVLTW1La01Gaw==')}`,
			},
		}
	);
	if (!res.ok) throw new Error(await res.text());
	// console.trace('query cost', res.headers.get('x-contentful-graphql-query-cost'));
	return (await res.json()).data;
}

/**
 * @typedef {object} Club
 * @property {string} slug
 * @property {string} name
 * @property {string | null} tent
 * @property {string | null} description
 * @property {string | null} meetingLocation
 * @property {string | null} meetingWhen
 * @property {string | null} grades
 * @property {string | null} clubWebsite
 * @property {string | null} listingWebsite
 * @property {string[] | null} tags
 */

/** @type {Club[]} */
let clubs = [];
const clubQuery = `{
	clubCollection(order: name_ASC) {
		items {
			slug
			name
			tent
			description
			meetingLocation
			meetingWhen
			grades
			clubWebsite
			listingWebsite
			tags
		}
	}
}`;
export async function getClubs() {
	if (clubs.length === 0) {
		clubs = (await queryContentful(clubQuery)).clubCollection.items;
	}
	return clubs;
}

export const sponsorTiers = /** @type {const} */ ([
	'clover',
	'sky',
	'gold',
	'silver',
	'bronze',
	'copper',
	'automobile',
	'custom',
	'friends-family',
	'business-card',
	'inkind',
]);

/** @param {(typeof sponsorTiers)[number]} tier */
export const sponsorTierName = (tier) =>
	tier === 'friends-family' ? 'Friends & Family'
	: tier === 'business-card' ? 'Business Card'
	: tier === 'inkind' ? 'In-Kind Donation'
	: tier.substring(0, 1).toUpperCase() + tier.substring(1);

/**
 * @typedef {object} Sponsor
 * @property {string} heading
 * @property {{ url: string } | null} image
 * @property {string | null} description
 * @property {string | null} link
 * @property {(typeof sponsorTiers)[number]} tier
 */

/** @type {Sponsor[]} */
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
