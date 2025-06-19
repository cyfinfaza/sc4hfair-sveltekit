import { getSponsors, sponsorTiers, sponsorTierName } from 'logic/contentful';

export async function load() {
	let sponsors = await getSponsors();
	let sorted = sponsorTiers
		.map((tier) => ({
			tier: sponsorTierName(tier),
			sponsors: sponsors.filter((sponsor) => sponsor.tier === tier),
		}))
		.filter((tier) => tier.sponsors.length > 0);

	return { sorted };
}
