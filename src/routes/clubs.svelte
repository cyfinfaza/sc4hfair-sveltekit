<script context="module">
	import { queryContentful } from 'logic/contentful.js';
	const query = `{
	clubCollection {
		items {
			slug
				name
				meetingLocation
				clubWebsite
				description
				grades
				meetingWhen
				listingWebsite
				tent
		}
	}
}`;
	export async function load({ fetch }) {
		const resp = await queryContentful(fetch, query);
		// console.log(resp);
		return { props: { clubs: resp.clubCollection?.items } };
	}
</script>

<script>
	import Layout from 'components/Layout.svelte';
	import { exactSearch } from 'logic/search.js';
	import ClubBox from 'components/ClubBox.svelte';
	export let clubs;
	// console.log(clubs);

	const isBrowser = typeof window !== 'undefined';

	let searchQuery = isBrowser ? localStorage.getItem('searchQuery') || '' : '';

	$: isBrowser && window.sessionStorage.setItem('clubs_search_query', JSON.stringify(searchQuery));

	let results = [];
	$: results = exactSearch(
		clubs,
		'name',
		['description', 'meetingWhen', 'meetingLocation', 'grades'],
		searchQuery
	);
</script>

<Layout title="Clubs">
	<div class="center">
		<h1>Clubs</h1>
		<p>
			Tap the +Add button to add a club to your interest list.{' '}
			<a href="/interests">View interest list</a>
		</p>
	</div>
	<div class="filterOptions">
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<button style:display={searchQuery != ''} on:click={(_) => (searchQuery = '')}>Clear</button>
	</div>
	<div class="columnCentered">
		{#each results as club}
			<ClubBox {club} />
		{/each}
	</div>
</Layout>

<style>
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

	.filterOptions input {
		width: 250px;
		text-indent: 4px;
	}
</style>
