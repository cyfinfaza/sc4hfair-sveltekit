<script>
	import Layout from 'components/Layout.svelte';
	import { exactSearch } from 'logic/search.js';
	import { goto } from '$app/navigation';

	export let data;

	let searchQuery = '',
		results = [];

	// todo: add ability to search inside items array
	$: results = exactSearch(data.foodVendors, 'name', [], searchQuery);
</script>

<Layout title="Food">
	<div class="center">
		<h1>Food Menu</h1>
		<p>A wide variety of food options are available from 4-H clubs and organizations.</p>
	</div>
	<div class="filterOptions">
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<button style:display={searchQuery ? null : 'none'} on:click={() => (searchQuery = '')}
			>Clear</button
		>
		<button on:click={() => goto('/map?locate=food')}>Locate Food Tent</button>
	</div>
	<div class="columnCentered">
		{#each results as vendor}
			<h2>{vendor.name}</h2>
			<table>
				{#each vendor.items as item}
					<tr>
						<td>{item.key}</td>
						<td>{item.value}</td>
					</tr>
				{/each}
			</table>
		{/each}
	</div>
</Layout>

<style lang="scss">
	.filterOptions {
		width: 100%;
		display: flex;
		justify-content: center;
		margin-bottom: 16px;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}
	.filterOptions > * {
		margin-block: 0;
	}

	h2 {
		text-align: center;
		margin-bottom: 8px;
	}

	table {
		width: 100%;
		max-width: 40ch;
		padding: 0 8px;

		td:last-child {
			text-align: right;
		}
	}
</style>
