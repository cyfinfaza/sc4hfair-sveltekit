<script>
	import ClubBox from 'components/ClubBox.svelte';
	import KioskPitch from 'components/KioskPitch.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import NoOffline from 'components/NoOffline.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	import { isOnline, kioskMode } from 'logic/stores.js';
	import {
		interestsSlugs,
		session,
		initSupabaseClient,
		logout,
		addInterest,
		removeInterest,
	} from 'logic/supabase.js';
	import { onMount } from 'svelte';

	export let data;

	let results = [];
	$: if ($interestsSlugs)
		results = data.clubs.filter((club) => $interestsSlugs.indexOf(club.slug) > -1);

	let reqLoginMessage = false;
	$: if ($session) reqLoginMessage = false;

	onMount(async () => {
		await initSupabaseClient();

		var searcher = new URLSearchParams(window.location.search);
		const [add, remove] = [searcher.get('add'), searcher.get('remove')];

		if (add) addInterest(add);
		if (remove) removeInterest(remove);
		if (searcher.get('reqLoginMessage') && !$session) reqLoginMessage = true;
	});

	$: console.log('Interests:', $interestsSlugs);
	$: console.log('Session:', $session);
</script>

<Layout title="Interest List">
	<div class="center">
		<h1>Interest List</h1>
		<p>Keep a list of clubs you are interested in</p>
		{#if $kioskMode}
			<KioskPitch />
		{:else}
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
					<LinkButton
						label={$isOnline ? 'Add Clubs to List' : 'View clubs'}
						icon="open_in_new"
						href="/clubs"
					/>
					<LinkButton label="Sign out" icon="logout" on:click={() => logout()} />
				{:else if !$isOnline}
					<NoOffline />
				{:else}
					<SignInButtons redirect="/interests" />
				{/if}
			</p>
		{/if}
	</div>
	<div class="columnCentered">
		{#if $session && !$isOnline && results.length === 0}
			<!-- in case the results weren't cached -->
			<NoOffline />
		{:else}
			{#each results as club}
				<ClubBox {club} />
			{/each}
		{/if}
	</div>
</Layout>
