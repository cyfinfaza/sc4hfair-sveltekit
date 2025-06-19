<script lang="ts">
	import { browser } from '$app/environment';
	import DateTime from 'components/DateTime.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import tentSlugs from 'data/tentSlugs.json';
	import { eventIsFuture } from 'logic/scheduling';
	import { kioskMode } from 'logic/stores.svelte';
	import { canWebShare, share } from 'logic/webshare';
	import { onMount, tick } from 'svelte';

	let {
		event,
		index = 0,
		subscribed = false,
		setEventSubscription,
	}: {
		event: import('./$types').PageData['events'][number];
		index?: number;
		subscribed?: boolean;
		setEventSubscription: (eventId: string, subscribed: boolean) => void;
	} = $props();

	const timeLabels = {
		past: {
			label: 'Past',
			style: 'background: var(--grey); color: var(--grey-text);',
		},
		future: {
			label: 'Scheduled',
			style: 'background: var(--yellow); color: var(--yellow-text);',
		},
		now: {
			label: 'Now',
			style: 'background: var(--green); color: var(--green-text);',
		},
	};
	let timeLabel: (typeof timeLabels)[keyof typeof timeLabels] = $state(timeLabels.now);
	if (!eventIsFuture(event)) timeLabel = timeLabels.past;
	else if (new Date(event.time) > new Date()) timeLabel = timeLabels.future;

	let targeted = $state(browser && window.location?.hash === '#' + event.sys.id),
		div: HTMLDivElement;

	const scrollIntoView = () => {
		if (window.location?.hash === '#' + event.sys.id) {
			div.scrollIntoView({ behavior: 'instant' });
		}
	};
</script>

<div
	bind:this={div}
	class:targeted
	class="container"
	id={event.sys.id}
	style:animation-delay={Math.min(index, 15) * 0.05 + 's'}
	onanimationstart={scrollIntoView}
	onanimationend={scrollIntoView}
>
	<div class="top">
		<h2>{event.title}</h2>
		<!-- {#if event.description}
			<p>{event.description}</p>
		{/if} -->
	</div>
	<div class="bottom">
		<div class="timeData">
			<h3>
				<div class="eventTimeLabel" style={timeLabel.style}>
					{timeLabel.label}
				</div>
				<DateTime date={event.time} calendar />
			</h3>
			{#if event.endTime}
				<p>
					<!-- <DateTime date={event.time} duration={event.endTime} /> long -->
					ends at <DateTime date={event.endTime} format="t" />
				</p>
			{/if}
		</div>
		<div class="buttonPanel">
			{#if event.tent}
				<LinkButton
					label={(event.near ? 'Near ' : '') + (tentSlugs[event.tent] || event.tent)}
					disabled={!tentSlugs[event.tent]}
					icon="place"
					href={`/map?locate=${event.tent}`}
				/>
			{/if}
			{#if $canWebShare}
				<LinkButton
					icon="share"
					onclick={() => {
						let loc = new URL(window.location.href);
						loc.hash = event.sys.id;
						share(event.title, loc.toString());
					}}
					lightFont
				/>
			{/if}
			{#if !$kioskMode}
				{@const hasStarted = Date.now() > new Date(event.time).getTime()}
				{@const alt =
					hasStarted ? 'Event already started'
					: subscribed ? 'Cancel notification'
					: 'Notify me'}
				<LinkButton
					class={subscribed ? 'jiggle' : ''}
					icon={subscribed ? 'notifications_active' : 'notifications_none'}
					active={subscribed}
					disabled={hasStarted}
					aria-label={alt}
					title={alt}
					onclick={() => setEventSubscription(event.sys.id, !subscribed)}
				/>
			{/if}
		</div>
	</div>
</div>

<style lang="scss">
	.container {
		width: 100%;
		border-radius: 8px;
		background-color: var(--light);
		padding: 12px;
		margin-bottom: 16px;
		box-sizing: border-box;
		animation: zoomin 0.5s backwards ease;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		background-size: cover;
		scroll-margin-top: calc(var(--nav-height) + 16px);

		> div * {
			margin: 0;
		}

		&.targeted {
			border: 2px solid var(--accent);
			// background: var(--light-2);
		}

		.eventTimeLabel {
			all: unset;
			font-weight: bold;
			font-size: 0.7em;
			text-transform: uppercase;
			padding: 2px 4px;
			margin-right: 6px;
			border-radius: 4px;
		}
	}

	.top {
		text-align: left;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 4px;

		h2 {
			margin: 0;
			word-wrap: break-word;
			hyphens: auto;
		}
		// for unused description
		// p {
		// 	margin-bottom: 4px;
		// }
	}

	.bottom {
		margin-top: 2em;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		justify-content: flex-end;
		gap: 8px;
	}

	.buttonPanel {
		display: flex;
		align-items: flex-end;
		justify-content: flex-end;
		flex-wrap: wrap;
		gap: 8px;
		// > :global(*) {
		// 	margin: 0;
		// }
	}

	.timeData {
		text-align: right;
		margin-left: auto !important;

		h3 {
			display: flex;
			align-items: center;
			justify-content: flex-end;
		}
	}

	@keyframes zoomin {
		0% {
			transform: scale(0.88);
			opacity: 0;
		}
	}

	@keyframes jiggle {
		0% {
			transform: rotate(-10deg);
		}
		50% {
			transform: rotate(10deg);
		}
		100% {
			transform: rotate(0deg);
		}
	}
	:global(.jiggle .material-icons) {
		animation: jiggle 0.5s ease-in-out 1;
	}
</style>
