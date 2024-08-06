<script>
	import { browser } from '$app/environment';
	import Layout from 'components/Layout.svelte';
	import ToggleButton from 'components/ToggleButton.svelte';
	import tentSlugs from 'data/tentSlugs.json';
	import { eventIsFuture } from 'logic/scheduling.js';
	import { exactSearch } from 'logic/search.js';
	import { kioskMode } from 'logic/stores.js';
	import EventBox from './EventBox.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

	let selectedTent = 'All';
	let showingPast = false;
	let searchQuery = '';
	/** @type {string[]} */
	let starredEvents = (browser && JSON.parse(localStorage.getItem('starredEvents') || '[]')) || [];
	let showingOnlyStarredEvents = false;

	$: browser && window.localStorage.setItem('starredEvents', JSON.stringify(starredEvents));

	/** @param {string} id */
	function toggleStarredEvent(id) {
		if (starredEvents.includes(id)) {
			starredEvents = starredEvents.filter((event) => event !== id);
		} else {
			starredEvents = [...starredEvents, id];
		}
	}

	let results = [];
	$: results = exactSearch(
		searchQuery,
		data.events.filter(
			(element) =>
				((selectedTent === 'All' || selectedTent === element.tent) &&
					(eventIsFuture(element) || showingPast)) ||
				(browser && window.location?.hash === '#' + element.sys.id)
		),
		'title',
		['tentName']
	).filter((element) => !showingOnlyStarredEvents || starredEvents.includes(element.sys?.id));
</script>

<Layout title="Schedule">
	<h1 class="center">Events</h1>
	<div class="filterOptions">
		<p>Filter:</p>
		<select bind:value={selectedTent} name="Tent">
			{#each data.eventTentsList as tent (tent)}
				<option value={tent}>
					{(tent !== 'All' && tentSlugs[tent]) || tent}
				</option>
			{/each}
		</select>
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<ToggleButton bind:value={showingPast}>Show Past Events</ToggleButton>
		{#if !$kioskMode}
			<ToggleButton bind:value={showingOnlyStarredEvents}>Show Only Starred Events</ToggleButton>
		{/if}
	</div>
	<div class="columnCentered">
		{#each results as event, i (event.sys.id)}
			<EventBox
				{event}
				index={i}
				starred={starredEvents.includes(event.sys.id)}
				{toggleStarredEvent}
			/>
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
</style>
