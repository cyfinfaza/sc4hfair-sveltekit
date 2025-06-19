<script lang="ts">
	import { browser } from '$app/environment';
	import { navigating } from '$app/state';
	// import FourH from 'assets/4h.svg?component';
	import Logo from 'assets/logo.svg?component';
	import LinkButton from 'components/LinkButton.svelte';
	import LoadingRing from 'components/LoadingRing.svelte';
	import SponsorSpot from 'components/SponsorSpot.svelte';
	import ThemeSwitcher from 'components/ThemeSwitcher.svelte';
	import { isOnline, menuOpen } from 'logic/stores.svelte';
	import 'styles/button.css';

	let { offsetContent = true } = $props();
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<nav
	class="invisible"
	style:height={offsetContent ? null : 0}
	onkeydown={(e) => {
		if (e.key === 'Escape') {
			menuOpen.set(false);
		}
	}}
>
	<div
		class="visible"
		style:height={$menuOpen ? '100vh' : ''}
		style:background={$isOnline ? 'var(--navbar)' : 'var(--navbar-grey)'}
	>
		<div class="topBar">
			<a
				href="/"
				aria-label="Main page"
				data-sveltekit-reload={true}
				onclick={() => (window.location.href = '/')}
			>
				<Logo />
			</a>
			<div class="horizPanel2" style:gap="12px">
				{#if !$isOnline}
					<span class="material-icons" aria-hidden="true">cloud_off</span>
				{/if}
				<LoadingRing loading={browser && navigating.type !== null} />
				<button type="button" class="menuButton button" onclick={() => ($menuOpen = !$menuOpen)}>
					<div class="menuIconContainer">
						<i class:inactive={$menuOpen} class="material-icons" aria-hidden="true">menu</i>
						<i class:inactive={!$menuOpen} class="material-icons" aria-hidden="true">close</i>
					</div>
					<span>Menu</span>
				</button>
			</div>
		</div>
		<div class="menuArea" id="menuArea" onfocusin={() => ($menuOpen = true)}>
			<div class="menuGrid">
				<LinkButton header label="Latest" icon="home" href="/" />
				<LinkButton header label="Map" icon="map" href="/map" />
				<LinkButton header label="Food" icon="fastfood" href="/food" />
				<LinkButton header label="Schedule" icon="event_note" href="/schedule" />
				<LinkButton header label="Clubs" icon="groups" href="/clubs" />
				<LinkButton header label="Scavenger Hunt" icon="travel_explore" href="/scavenger-hunt" />
			</div>
			<div class="menuBottom">
				<ThemeSwitcher header />
				<LinkButton headerSmall label="Settings" icon="settings" href="/settings" />
				<LinkButton
					headerSmall
					disabled={!$isOnline}
					label="App feedback"
					icon="message"
					href="/feedback"
				/>
				<LinkButton headerSmall label="Interest list" icon="list_alt" href="/interests" />
				<LinkButton headerSmall label="Fair sponsors" icon="monetization_on" href="/sponsors" />
				<!-- <LinkButton headerSmall disabled={!$isOnline} label="About 4‑H" href="https://4histops.org">
					<svelte:fragment slot="iconElement">
						<FourH
							style="height: 100%; fill: currentColor; transition: fill var(--theme-transition);"
						/>
					</svelte:fragment>
				</LinkButton> -->
				<LinkButton headerSmall label="Links" icon="link" href="/links" />
			</div>
			<div class="dqpmdptSpot">
				<SponsorSpot />
			</div>
		</div>
	</div>
</nav>

<style lang="scss">
	.visible {
		width: 100%;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		height: var(--nav-height);
		position: fixed;
		top: 0;
		left: 0;
		transition: 300ms cubic-bezier(0.075, 0.82, 0.165, 1);
		backdrop-filter: var(--backdrop-blur);
		background: var(--navbar);
		z-index: 999;
		box-shadow: var(--button-shadow);
	}

	.invisible {
		width: 100%;
		height: var(--nav-height);
	}

	.topBar {
		height: var(--nav-height);
		display: flex;
		justify-content: space-between;
		padding: 16px;
		box-sizing: border-box;

		:global(svg) {
			height: 100%;
			fill: currentColor;
			transition: fill var(--theme-transition);
			cursor: pointer;
		}
	}

	.menuArea {
		flex: 1;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		text-align: center;
		align-items: center;
		padding: 16px;
		gap: 24px;
	}

	// Prevents text being shifted during the transition when the height gets too small
	.menuArea::-webkit-scrollbar {
		width: 0;
	}

	.menuGrid {
		width: 100%;
		/* color: var(--navbar-text); */
		display: flex;
		gap: 16px;
		align-items: flex-start;
		justify-content: center;
		flex-wrap: wrap;
	}

	.menuBottom {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 12px;

		> :global(*) {
			white-space: nowrap;
		}
	}

	.menuButton {
		justify-self: flex-end;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		border: none;
		padding: 8px;
		border-radius: 8px;
		/* color: var(--navbar-text); */
		background-color: var(--navbar-accent);
		// outline: none;
		/* cursor: pointer; */
		/* user-select: none; */
		/* box-shadow: 0 0 6px 0px #0008; */
		/* -webkit-tap-highlight-color: rgba(0, 0, 0, 0); */
		/* transition: (filter, transform) 120ms ease; */

		& > span {
			margin-left: 6px;
			font-weight: bold;
			font-size: 18px;
		}
	}

	.menuIconContainer {
		width: 24px;
		height: 24px;
		position: relative;

		& * {
			position: absolute;
			height: 24px;
			width: 24px;
			margin: 0;
			top: 0;
			left: 0;
			transition: transform 240ms ease;
		}

		& i.inactive {
			transform: scale(0.6);
			opacity: 0;
		}
	}

	.button {
		background-color: var(--navbar-accent);
	}

	.dqpmdptSpot {
		width: 100%;
		max-width: 500px;
		box-sizing: border-box;
		--spsp-bg: var(--navbar-accent);
	}
</style>
