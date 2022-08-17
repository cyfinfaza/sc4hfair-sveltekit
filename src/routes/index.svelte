<script context="module">
	import { queryContentful } from 'logic/contentful.js';
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
	export async function load({ fetch }) {
		return { props: { posts: (await queryContentful(fetch, query)).postCollection?.items } };
	}
</script>

<script>
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Post from 'components/Post.svelte';
	import { isStandalone } from 'logic/platform.js';
	import { menuOpen } from 'logic/stores.js';
	import { onMount } from 'svelte';

	export let posts;

	let showInstallBox = false;
	onMount(() => {
		if (!isStandalone() && localStorage.getItem('installBox') !== '1') showInstallBox = true;
	});
</script>

<Layout>
	<h1 class="center">Welcome to the Somerset County 4-H Fair.</h1>
	{#if showInstallBox}
		<div class="installBox">
			<strong>Finish installing the fair app by adding it to your home screen:</strong>
			<InstallInstructions />
			<p>
				<strong>
					You can find these instructions later in <a href="/settings">settings</a>.
				</strong>
				<LinkButton
					icon="close"
					label="Dismiss"
					acrylic
					on:click={() => {
						showInstallBox = false;
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
	}
</style>
