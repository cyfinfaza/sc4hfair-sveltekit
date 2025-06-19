<script lang="ts">
	import Layout from 'components/Layout.svelte';
	import SponsorSpot from 'components/SponsorSpot.svelte';

	let { data } = $props();
</script>

<Layout title="Sponsors">
	<div class="center">
		<h1>Sponsors</h1>
		<p>The 4-H fair is made possible by our sponsors.</p>
	</div>
	<div class="columnCentered">
		{#each data.sorted as tier}
			{#if tier.sponsors.length}
				<h2>{tier.tier}</h2>
				{#each tier.sponsors as sponsor}
					<SponsorSpot {sponsor} listMode />
				{/each}
			{/if}
		{/each}
	</div>
</Layout>
