<script context="module">
	import { getSponsors } from 'logic/contentful.js';
	export async function load({ fetch }) {
		const resp = await getSponsors(fetch);
		return { props: { sponsors: resp } };
	}
</script>

<script>
	import Layout from 'components/Layout.svelte';
	import SponsorSpot from 'components/SponsorSpot.svelte';
	export let sponsors;

	const isBrowser = typeof window !== 'undefined';
</script>

<Layout title="Clubs">
	<div class="center">
		<h1>Sponsors</h1>
		<p>The 4-H fair is made possible by our sponsors.</p>
	</div>
	<div class="columnCentered">
		{#each ['Gold', 'Silver', 'Bronze'] as tier}
			<h2>{tier}</h2>
			{#each sponsors.filter((sponsor) => sponsor.tier === tier.toLowerCase()) as sponsor}
				<SponsorSpot {sponsor} listMode />
			{/each}
		{/each}
	</div>
</Layout>
