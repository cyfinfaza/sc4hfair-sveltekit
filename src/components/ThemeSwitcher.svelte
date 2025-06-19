<script lang="ts">
	import LinkButton from 'components/LinkButton.svelte';
	import { theme, themes } from 'logic/theming';

	let { header = false } = $props();

	let currentTheme = $derived(themes.find((item) => item.id === $theme) || themes[0]);

	let nextThemeID = $derived.by(() => {
		const currentIndex = themes.indexOf(currentTheme);
		return currentIndex === -1 || currentIndex === themes.length - 1 ?
				themes[0].id
			:	themes[currentIndex + 1].id;
	});
</script>

<LinkButton
	onclick={() => ($theme = nextThemeID)}
	label="Switch theme"
	lightFont
	noCloseHeader
	headerSmall={header}
>
	{#snippet iconElement()}
		{#key $theme}
			<span class="material-icons icon" aria-hidden="true" aria-label={currentTheme.name}>
				{currentTheme.icon}
			</span>
		{/key}
	{/snippet}
</LinkButton>

<style>
	.icon {
		transition: transform 650ms ease;
		animation: spinney 650ms ease;
	}
	@keyframes spinney {
		0% {
			transform: rotate(-360deg);
		}
	}
</style>
