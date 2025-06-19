<script lang="ts">
	import ClubBox from 'components/ClubBox.svelte';
	import KioskPitch from 'components/KioskPitch.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import NoOffline from 'components/NoOffline.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	import { logout, session } from 'logic/auth';
	import { addInterest, initInterests, interestsSlugs, removeInterest } from 'logic/interests';
	import { isOnline, kioskMode } from 'logic/stores.svelte';
	import { onMount } from 'svelte';

	let { data } = $props();

	let results = $derived(
		$interestsSlugs ? data.clubs.filter((club) => $interestsSlugs.indexOf(club.slug) > -1) : []
	);

	let reqLoginMessage = $state(false);
	$effect(() => {
		if ($session) reqLoginMessage = false;
	});

	onMount(async () => {
		initInterests();

		var searcher = new URLSearchParams(window.location.search);
		const [add, remove] = [searcher.get('add'), searcher.get('remove')];

		if (add) addInterest(add);
		if (remove) removeInterest(remove);
		if (searcher.get('reqLoginMessage') && !$session) reqLoginMessage = true;
	});
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
					Signed in as <strong>{$session.email}</strong>
				{:else}
					You are not signed in.
				{/if}
			</p>
			{#if reqLoginMessage}
				<p style="color: red;">Sign in to add this item to your interest list.</p>
			{/if}
			<div class="horizPanel margin">
				{#if $session}
					<LinkButton
						label={$isOnline ? 'Add Clubs to List' : 'View clubs'}
						icon="open_in_new"
						href="/clubs"
					/>
					<LinkButton label="Sign out" icon="logout" onclick={() => logout()} />
				{:else if !$isOnline}
					<NoOffline />
				{:else}
					<SignInButtons redirect="/interests" />
				{/if}
			</div>
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
