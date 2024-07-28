<script>
	import Layout from 'components/Layout.svelte';
	import { exactSearch } from 'logic/search.js';
	import { goto } from '$app/navigation';

	export let data;

	let searchQuery = '',
		results = [];

	$: results = exactSearch(searchQuery, data.foodVendors, 'name', ['name'], true);
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
			{#if vendor.items.length}
				<h2>{vendor.name}</h2>
				<ul>
					{#each vendor.items as item}
						<li>
							<span>{item.key}</span>
							<span>{item.value}</span>
						</li>
					{/each}
				</ul>
			{/if}
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

	ul {
		width: 100%;
		max-width: 40ch;
		padding: 0 8px;

		padding: 0;
		overflow-x: hidden;
		list-style: none;

		li span {
			background-color: var(--bg);
		}
		li :first-child {
			padding-right: 0.33ch;

			&:after {
				content: ' . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .';
				float: left;
				width: 0;
				white-space: nowrap;
				color: var(--text-translucent);
			}
		}
		li :last-child {
			padding-left: 0.33ch;
			float: right;
			text-align: right;
		}
	}
</style>
