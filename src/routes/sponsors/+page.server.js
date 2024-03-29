import { getSponsors } from 'logic/contentful.js';

const tiers = ['sky', 'gold', 'silver', 'bronze', 'automobile', 'custom', 'friends-family'];

export async function load() {
	let sponsors = await getSponsors();
	let sorted = tiers.map((tier) => ({
		tier:
			tier === 'friends-family'
				? 'Friends & Family'
				: tier.substring(0, 1).toUpperCase() + tier.substring(1),
		sponsors: sponsors.filter((sponsor) => sponsor.tier === tier),
	}));

	return { sorted };
}
