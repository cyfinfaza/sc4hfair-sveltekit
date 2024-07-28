<script>
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
</script>

<Layout title="Links">
	<div class="center">
		<h1>Links</h1>
		<p>Links to various 4‑H fair related resources.</p>
	</div>
	<div class="columnCentered">
		<div class="box">
			<h2>4‑H Website</h2>
			<p>The 4‑H website includes additional information about 4‑H activities year-round.</p>
			<LinkButton icon="open_in_new" external href="https://4histops.org" label="Open link" />
		</div>
		<div class="box">
			<h2>Want Your Project Here?</h2>
			<p>
				For 4‑H clubs: If you're working on a project applicable to all fair visitors, let us know
				so we can add your link here.
			</p>
			<LinkButton icon="message" href="/feedback" label="Contact us" />
		</div>
	</div>
</Layout>

<style lang="scss">
	.box {
		width: 100%;
		border-radius: 8px;
		background-color: var(--light);
		padding: 12px;
		margin-bottom: 16px;
		box-sizing: border-box;

		h2 {
			margin: 0;
			margin-bottom: 0.25em;
		}
		p {
			margin: 0.5em 0;
		}

		& :global(> :last-child) {
			margin-top: 0.75em;
			float: right;
		}
	}
</style>
