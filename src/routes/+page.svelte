<script>
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Post from 'components/Post.svelte';
	import { queryContentful } from 'logic/contentful.js';
	import { isStandalone } from 'logic/platform.js';
	import { menuOpen } from 'logic/stores.js';
	import { onMount } from 'svelte';
	import { checkNotificationStatus, subscribe } from 'logic/webpush';
	import NotificationEnableButton from 'components/NotificationEnableButton.svelte';

	const query = `{
	postCollection(order:sys_firstPublishedAt_DESC) {
		items {
			title
			contentText
			sys {
				publishedAt
			}
		}
	}
}`;

	let posts = [];
	onMount(async () => {
		posts = (await queryContentful(query)).postCollection?.items;
	});

	let showSetupBox = false;
	onMount(() => {
		if (localStorage.getItem('installBox') !== '1') showSetupBox = true;
	});
</script>

<Layout>
	<h1 class="center">Welcome to the Somerset County 4-H Fair.</h1>
	{#if showSetupBox}
		<div class="installBox">
			<h3 style="text-align: center">Finish setting up the fair app</h3>
			<hr />
			<strong>Add the fair app to your homescreen:</strong>
			<InstallInstructions />
			{#await checkNotificationStatus() then registered}
				{#if true}
					<strong>Enable notifications about fair updates:</strong>
					<p style="display: flex; align-items: center; gap: 8px;">
						<NotificationEnableButton />
					</p>
				{/if}
			{/await}
			<hr />
			<p>
				<strong>
					You can find these options later in <a href="/settings">settings</a>.
				</strong>
				<LinkButton
					icon="close"
					label="Dismiss"
					acrylic
					on:click={() => {
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
		<LinkButton label="More" icon="add" on:click={() => ($menuOpen = true)} />
	</div>
	<h2 class="center">Latest Updates</h2>
	<div clas="columnCentered">
		{#each posts as post, i}
			<Post data={post} index={i} />
		{/each}
	</div>
</Layout>

<style lang="scss">
	.installBox {
		width: 100%;
		border-radius: 8px;
		padding: 12px;
		margin-bottom: 20px;
		box-sizing: border-box;
		border: 2px solid var(--text-translucent);
		display: flex;
		flex-direction: column;
		gap: 8px;
		> :global(*) {
			margin: 0;
		}
		> :last-child {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 8px;
			:global(button) {
				white-space: nowrap;
			}
		}
		.numberCircle {
			padding: 8px;
			box-sizing: border-box;
			height: 1em;
			border-radius: 0.5em;
			background-color: var(--text);
			color: var(--bg);
		}
		hr {
			border-color: var(--light);
			border-width: 2px;
			margin-top: 4px;
			margin-bottom: 4px;
		}
	}
</style>
