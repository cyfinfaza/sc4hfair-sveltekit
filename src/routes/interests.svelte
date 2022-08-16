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
	import {
		interestsSlugs,
		session,
		initSupabaseClient,
		login,
		logout,
		addInterest,
		removeInterest,
	} from 'logic/supabase.js';
	import { onMount } from 'svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	export let clubs;
	// console.log(clubs);

	const isBrowser = typeof window !== 'undefined';

	let searchQuery = isBrowser ? localStorage.getItem('searchQuery') || '' : '';

	$: isBrowser && window.sessionStorage.setItem('clubs_search_query', JSON.stringify(searchQuery));

	let results = [];
	$: if ($interestsSlugs) results = clubs.filter((club) => $interestsSlugs.indexOf(club.slug) > -1);

	let reqLoginMessage = false;

	$: if ($session) reqLoginMessage = false;

	onMount(async () => {
		await initSupabaseClient();
		var searcher = new URLSearchParams(window.location.search);
		const [add, remove] = [searcher.get('add'), searcher.get('remove')];
		if (add) {
			addInterest(add);
		}
		if (remove) {
			removeInterest(remove);
		}
		if (searcher.get('reqLoginMessage') && !$session) {
			reqLoginMessage = true;
		}
	});

	$: console.log('Interests: ', $interestsSlugs);
	$: console.log('Session: ', $session);
</script>

<Layout title="Interest List">
	<div class="center">
		<h1>Interest List</h1>
		<p>Keep a list of clubs you are interested in</p>
		<p>
			{#if $session}
				Signed in as <strong>{$session.user.email}</strong>
			{:else}
				You are not signed in.
			{/if}
		</p>
		{#if reqLoginMessage}
			<p style="color: red;">Sign in to add this item to your interest list.</p>
		{/if}
		<p class="horizPanel" style="white-space: nowrap;">
			{#if $session}
				<LinkButton label="Add Clubs to List" icon="open_in_new" href="/clubs" />
				<LinkButton label="Sign out" icon="logout" on:click={() => logout()} />
			{:else}
				<SignInButtons redirect="/interests" />
			{/if}
		</p>
	</div>
	<div class="columnCentered">
		{#each results as club}
			<ClubBox {club} />
		{/each}
	</div>
</Layout>

<style>
</style>
