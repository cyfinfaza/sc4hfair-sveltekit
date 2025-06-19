<script lang="ts">
	import { goto } from '$app/navigation';
	import Layout from 'components/Layout.svelte';
	import { exactSearch } from 'logic/search';

	let { data } = $props();

	let searchQuery = $state(''),
		results = $derived(exactSearch(searchQuery, data.foodVendors, 'name', ['name'], true));
</script>

<Layout title="Food">
	<div class="center">
		<h1>Food Menu</h1>
		<p>A wide variety of food options are available from 4-H clubs and organizations.</p>
	</div>
	<div class="filterOptions">
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<button style:display={searchQuery ? null : 'none'} onclick={() => (searchQuery = '')}
			>Clear</button
		>
		<button onclick={() => goto('/map?locate=food')}>Locate Food Tent</button>
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

		> * {
			margin-block: 0;
		}
	}

	h2 {
		text-align: center;
		margin: 4px 0;
	}

	ul {
		width: 100%;
		max-width: 40ch;
		padding: 0 8px;

		padding: 0;
		overflow-x: hidden;
		list-style: none;

		li {
			display: flex;

			// span {
			// 	background: var(--bg);
			// }
			:first-child {
				padding-right: 0.66ch;
			}
			:last-child {
				padding-left: 0.66ch;
				text-align: right;
				order: 2;
			}
			&:before {
				content: '';
				order: 1;
				flex-grow: 1;

				// content: '.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .';
				// width: 0;
				// white-space: nowrap;
				// color: var(--text-translucent);

				// transform: translateY(-30%);
				margin-bottom: 0.3em;
				border-bottom: dotted 0.25ch var(--text-translucent);
			}
		}
	}
</style>
