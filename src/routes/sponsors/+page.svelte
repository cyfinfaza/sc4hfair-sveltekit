<script>
	import Layout from 'components/Layout.svelte';
	import SponsorSpot from 'components/SponsorSpot.svelte';

	export let data;
</script>

<Layout title="Sponsors">
	<div class="center">
		<h1>Sponsors</h1>
		<p>The 4-H fair is made possible by our sponsors.</p>
	</div>
	<div class="columnCentered">
		{#each ['Gold', 'Silver', 'Bronze'] as tier}
			<h2>{tier}</h2>
			{#each data.sponsors.filter((sponsor) => sponsor.tier === tier.toLowerCase()) as sponsor}
				<SponsorSpot {sponsor} listMode />
			{/each}
		{/each}
	</div>
</Layout>
