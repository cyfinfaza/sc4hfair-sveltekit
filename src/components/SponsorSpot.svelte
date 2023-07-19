<script>
	import LinkButton from 'components/LinkButton.svelte';
	import { getContext } from 'svelte/internal';
	import { isOnline } from 'logic/stores.js';
	export let listMode = false;
	export let sponsor;
	let sponsors = getContext('sponsors');

	const DEFAULT_SPONSOR_DESCRIPTION = 'The 4‑H fair is made possible by our sponsors.';

	$: {
		if (!sponsor) {
			// let chosenTier = Math.random();
			// if (chosenTier < 0.45) chosenTier = 'gold'; // 45% chance
			// else if (chosenTier < 0.8) chosenTier = 'silver'; // 35% chance
			// else chosenTier = 'bronze'; // 20% chance
			// let filteredSponsors = sponsors.filter((ad) => ad.tier === chosenTier);

			sponsor = sponsors[Math.floor(Math.random() * sponsors.length)];
		}
	}
</script>

{#if sponsor}
	<div class="container" class:listMode>
		<picture>
			<source srcset={`${sponsor.image.url}?w=100&fm=webp`} type="image/webp" />
			<source srcset={`${sponsor.image.url}?w=100`} />
			<img alt="" src={sponsor.image.url} class="sfImage" />
		</picture>
		<div class="sfText">
			<h2>
				{#if !listMode}
					<span class="disclosure">
						{sponsor.tier ? sponsor.tier.charAt(0).toUpperCase() + sponsor.tier.slice(1) + ' ' : ''}
						Fair Sponsor
					</span>
				{/if}
				{sponsor.heading}
			</h2>
			{#if sponsor.description}
				<p>{sponsor.description.description}</p>
			{:else if !listMode}
				<p>{DEFAULT_SPONSOR_DESCRIPTION}</p>
			{/if}
			{#if sponsor.link}
				<LinkButton
					href={sponsor.link}
					disabled={!$isOnline}
					label="Visit"
					icon="open_in_new"
					headerSmall
					noCloseHeader
				/>
			{/if}
		</div>
	</div>
{/if}

<style lang="scss">
	.container {
		display: flex;
		width: 100%;
		// height: 100px;
		gap: 12px;
		background-color: var(--spsp-bg);
		padding: 12px;
		border-radius: 16px;
		box-sizing: border-box;
	}

	.container.listMode {
		background-color: var(--light);
		margin-bottom: 12px;
	}

	.sfImage {
		height: 100px;
		width: 100px;
		border-radius: 8px;
		object-fit: contain;
		background-color: white;
		padding: 4px;
		box-sizing: border-box;
	}

	.sfText {
		text-align: left;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 6px;
		// padding: 8px;
		> * {
			margin: 0;
		}
		> h2 {
			font-size: 1.2rem;
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			gap: 6px;
			margin: -2px 0;
		}
	}

	.disclosure {
		font-size: 0.8rem;
		border-radius: 4px;
		padding: 3px 6px;
		background-color: var(--navbar-accent);
		text-transform: uppercase;
		transition: background-color var(--theme-transition);
	}
</style>
