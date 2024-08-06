import { getSponsors, sponsorTiers } from 'logic/contentful.js';

export async function load() {
	let sponsors = await getSponsors();
	let sorted = sponsorTiers
		.map((tier) => ({
			tier:
				tier === 'friends-family' ? 'Friends & Family' : (
					tier.substring(0, 1).toUpperCase() + tier.substring(1)
				),
			sponsors: sponsors.filter((sponsor) => sponsor.tier === tier),
		}))
		.filter((tier) => tier.sponsors.length > 0);

	return { sorted };
}
