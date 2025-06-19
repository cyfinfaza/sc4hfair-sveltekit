<script lang="ts">
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Post from 'components/Post.svelte';
	import { queryContentful } from 'logic/contentful';
	import { isStandalone } from 'logic/platform';
	import { kioskMode, menuOpen } from 'logic/stores.svelte';
	import { notificationStatus } from 'logic/webpush';
	import { onMount } from 'svelte';
	import NotificationEnableButton from 'components/NotificationEnableButton.svelte';

	const query = `{
	postCollection(order:sys_firstPublishedAt_DESC) {
		items {
			title
			contentText
			sys {
				id
				publishedAt
			}
		}
	}
}`;

	let posts: import('logic/contentful').Post[] = $state([]);
	onMount(async () => {
		posts = (await queryContentful(query)).postCollection?.items;
	});

	let showSetupBox = $state(false);
	onMount(() => {
		if (localStorage.getItem('installBox') !== '1') showSetupBox = true;
	});
</script>

<Layout>
	{#if !$kioskMode}
		<h1 class="center">Welcome to the Somerset County 4‑H Fair.</h1>
		{#if showSetupBox}
			<div class="installBox">
				<h2 style="text-align: center">Finish setting up the fair app</h2>
				<hr />
				<strong>
					<span class="numberSquircle">
						1{#if $isStandalone}
							{' '}<span class="material-icons" aria-label="Done">check</span>
						{/if}
					</span>
					{' '}Add the fair app to your homescreen{$isStandalone ? '.' : ':'}
				</strong>
				{#if !$isStandalone}
					<InstallInstructions />
				{/if}
				<strong>
					<span class="numberSquircle">
						2{#if $notificationStatus?.registered}
							{' '}<span class="material-icons" aria-label="Done">check</span>
						{/if}
					</span>
					{' '}Enable notifications about fair updates:
				</strong>
				<p style="display: flex; align-items: center; gap: 8px;">
					<NotificationEnableButton />
				</p>
				<hr />
				<p class="bottom">
					<strong>
						You can find these options later in <a href="/settings">settings</a>.
					</strong>
					<LinkButton
						icon="close"
						label="Dismiss"
						acrylic
						onclick={() => {
							showSetupBox = false;
							localStorage.setItem('installBox', '1');
						}}
					/>
				</p>
			</div>
		{/if}
		<div class="horizPanel">
			<LinkButton label="Schedule" icon="event_note" href="/schedule" />
			<LinkButton label="Map" icon="map" href="/map" />
			<LinkButton label="More" icon="add" onclick={() => ($menuOpen = true)} />
		</div>
	{/if}
	<h2 class="center">Latest Updates</h2>
	{#each posts as post, i}
		<Post data={post} index={i} />
	{/each}
</Layout>

<style lang="scss">
	.installBox {
		> .bottom {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 8px;
			:global(button) {
				white-space: nowrap;
			}
		}
		.numberSquircle {
			padding: 0px 8px;
			box-sizing: border-box;
			border-radius: 0.5em;
			background-color: var(--text);
			color: var(--bg);
			.material-icons {
				font-size: 21px; // kinda jank but makes it appear the same size as the text
			}
		}
	}
</style>
