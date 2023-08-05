<script>
	import FourH from 'assets/4h.svg?component';
	import LinkButton from 'components/LinkButton.svelte';
	import { getContext } from 'svelte/internal';
	import { isOnline } from 'logic/stores.js';
	export let listMode = false;
	export let sponsor;
	let sponsors = getContext('sponsors');

	const DEFAULT_SPONSOR_DESCRIPTION = 'The 4‑H fair is made possible by our sponsors.';

	$: {
		if (!sponsor) {
			let chosenTier = Math.random();

			// because not all tiers are used this year, split into the mainer ones
			if (chosenTier < 0.25) chosenTier = ['sky']; // 25% but from one
			else if (chosenTier < 0.8) chosenTier = ['gold', 'silver', 'bronze']; // 55% the rest
			else chosenTier = ['custom', 'automobile', 'friends-family']; // 20% but from many

			let filteredSponsors = sponsors.filter((ad) => chosenTier.includes(ad.tier));

			sponsor = filteredSponsors[Math.floor(Math.random() * filteredSponsors.length)];
		}
	}
</script>

{#if sponsor}
	<div class="container" class:listMode>
		{#if sponsor.image}
			<picture>
				<source srcset={`${sponsor.image.url}?w=100&fm=webp`} type="image/webp" />
				<source srcset={`${sponsor.image.url}?w=100`} />
				<img alt="" src={sponsor.image.url} class="sfImage" />
			</picture>
		{:else}
			<FourH class="sfImage" style="fill: var(--accent)" />
		{/if}
		<div class="sfText">
			<h2>
				{#if !listMode}
					<span class="disclosure">
						{sponsor.tier
							? (sponsor.tier === 'friends-family' ? 'FRIENDS & FAMILY' : sponsor.tier) + ' '
							: ''}FAIR SPONSOR
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
					external
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

	:global(.sfImage) {
		height: 100px;
		// width: 100px;
		min-height: 100px;
		min-width: 100px;
		aspect-ratio: 1 / 1;
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
