<script lang="ts">
	import SvelteMarkdown from '@humanspeak/svelte-markdown';
	import EmptyComponent from 'components/EmptyComponent.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { interestsSlugs, removeInterest } from 'logic/interests';
	import { isOnline, kioskMode } from 'logic/stores.svelte';
	import { onMount, tick } from 'svelte';

	let { club, autoTarget = false } = $props();

	let div: HTMLDivElement;

	onMount(async () => {
		await tick();
		if (autoTarget) {
			div.scrollIntoView();
		}
	});
</script>

<div id={club.slug} bind:this={div} class:targeted={autoTarget} class="clubEntry">
	<h2>
		<span>{club.name}</span>
		<div class="tags">
			{#each club.tags as tag}
				<div title={tag.toUpperCase()}>{tag}</div>
			{/each}
		</div>
	</h2>
	<div class="description">
		<SvelteMarkdown renderers={{ image: EmptyComponent }} source={club.description} />
	</div>
	<div class="actionButtonsPanel">
		{#if club.tent}
			<LinkButton label="Map" icon="place" href={`/map?locate=${club.tent}`} lightFont />
		{/if}
		{#if !$kioskMode}
			{#if ($interestsSlugs || []).indexOf(club.slug) > -1}
				<LinkButton
					label="Remove"
					disabled={!$isOnline}
					icon="remove"
					onclick={() => removeInterest(club.slug)}
					lightFont
				/>
			{:else}
				<LinkButton
					label="Add"
					disabled={!$isOnline}
					icon="add"
					href={`/interests?add=${club.slug}`}
					lightFont
				/>
			{/if}
		{/if}
		<LinkButton label="View" icon="open_in_new" href={`/club/${club.slug}`} lightFont />
	</div>
</div>

<style lang="scss">
	.clubEntry {
		width: 100%;
		border-radius: 8px;
		background-color: var(--light);
		--entry-padding: 12px;
		padding: var(--entry-padding);
		margin-bottom: 16px;
		overflow: hidden;
		position: relative;
		box-sizing: border-box;

		&.targeted {
			border: 2px solid var(--accent);
		}

		> :global(*),
		> .description > :global(*) {
			margin: 0;
		}

		> h2 {
			text-transform: uppercase;
			display: flex;
			align-items: center;
			flex-wrap: wrap;

			@media (max-width: 600px) {
				// force all tags to be on a new line
				flex-direction: column;
				align-items: unset;
				justify-content: center;
			}

			> span {
				flex-grow: 1;
			}

			.tags {
				font-size: 0.6em;
			}
		}

		> .description {
			/* height: 64px; */
			width: calc(100% - var(--entry-padding) * 2);
			position: absolute;

			&:before {
				content: '';
				width: 100%;
				height: 100%;
				position: absolute;
				left: 0;
				top: 0;
				background: linear-gradient(transparent 20px, var(--light) 98px);
				/* TODO make this also have a nice transition */
				transition: background var(--theme-transition);
			}
		}
	}

	.actionButtonsPanel {
		margin-top: 48px;
		display: flex;
		width: 100%;
		justify-content: flex-end;
		z-index: 20;
		position: relative;
		gap: 8px;
	}
</style>
