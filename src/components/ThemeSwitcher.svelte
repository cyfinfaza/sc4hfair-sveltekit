<script>
	import LinkButton from 'components/LinkButton.svelte';
	import { theme, themes } from 'logic/theming';

	export let header = false;

	/** @type {import('logic/theming').ThemeId} */
	let nextThemeID,
		/** @type {import('logic/theming').themes[number]} */
		currentTheme,
		/** @type {HTMLSpanElement} */
		themeIcon;
	$: {
		currentTheme =
			themes.filter((item, index) => {
				if (item.id === $theme) {
					nextThemeID = themes.length - 1 === index ? themes[0].id : themes[index + 1].id;
					return true;
				}
				return false;
			})[0] || themes[0];
		if (themeIcon) {
			themeIcon.classList.remove('animate');
			themeIcon.classList.add('animate');
		}
	}
</script>

<LinkButton
	on:click={() => ($theme = nextThemeID)}
	label="Switch theme"
	lightFont
	noCloseHeader
	headerSmall={header}
>
	<svelte:fragment slot="iconElement">
		{#key $theme}
			<span
				class="material-icons icon"
				aria-hidden="true"
				aria-label={currentTheme.name}
				bind:this={themeIcon}
			>
				{currentTheme.icon}
			</span>
		{/key}
	</svelte:fragment>
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
