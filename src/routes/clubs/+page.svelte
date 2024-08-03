<script>
	import ClubBox from 'components/ClubBox.svelte';
	import Layout from 'components/Layout.svelte';
	import { exactSearch } from 'logic/search.js';
	import { isOnline, kioskMode } from 'logic/stores.js';
	import { browser } from '$app/environment';

	export let data;

	let searchQuery = (browser && window.sessionStorage.getItem('clubs_searchQuery')) || '';
	$: if (browser) window.sessionStorage.setItem('clubs_searchQuery', searchQuery);

	let results = [];
	$: results = exactSearch(searchQuery, data.clubs, 'name', [
		'description',
		'meetingWhen',
		'meetingLocation',
		'grades',
		'tags',
	]);
</script>

<Layout title="Clubs">
	<div class="center">
		<h1>Clubs</h1>
		{#if !$kioskMode}
			<p>
				Tap the +Add button to add a club to your interest list.
				{#if $isOnline}<a href="/interests">View interest list</a>{/if}
			</p>
		{/if}
	</div>
	<div class="filterOptions">
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<button style:display={searchQuery ? null : 'none'} on:click={() => (searchQuery = '')}
			>Clear</button
		>
	</div>
	<div class="columnCentered">
		{#each results as club}
			<ClubBox {club} autoTarget={browser && window.location?.hash === '#' + club.slug} />
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
