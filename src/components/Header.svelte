<script>
	import 'styles/button.css';
	import LinkButton from 'components/LinkButton.svelte';
	import LoadingRing from 'components/LoadingRing.svelte';
	import { navigating } from '$app/stores';
	import Logo from 'assets/logo.svg';
	import FourH from 'assets/4h.svg';
	import { menuOpen, isOnline } from 'logic/stores';
	import ThemeSwitcher from 'components/ThemeSwitcher.svelte';
	import SponsorSpot from 'components/SponsorSpot.svelte';
	export let offsetContent = true;
</script>

<div class="invisible" style:height={offsetContent ? null : 0}>
	<div
		class="visible"
		style:height={$menuOpen ? '100vh' : ''}
		style:background={$isOnline ? 'var(--navbar)' : 'var(--navbar-grey)'}
	>
		<div class="topBar">
			<Logo role="button" onclick="window.location.href = '/'" />
			<div class="horizPanel2" style:gap="12px">
				{#if !$isOnline}
					<span class="material-icons">cloud_off</span>
				{/if}
				<LoadingRing loading={$navigating} />
				<button type="button" class="menuButton button" on:click={(_) => ($menuOpen = !$menuOpen)}>
					<div class="menuIconContainer">
						<i class="material-icons" class:inactive={$menuOpen}>menu</i>
						<i class="material-icons" class:inactive={!$menuOpen}>close</i>
					</div>
					<span>Menu</span>
				</button>
			</div>
		</div>
		<div class="menuArea">
			<div class="menuGrid">
				<LinkButton header label="Latest" icon="home" href="/" />
				<LinkButton header label="Map" icon="map" href="/map" />
				<LinkButton header label="Schedule" icon="event_note" href="/schedule" />
				<LinkButton header label="Clubs" icon="groups" href="/clubs" />
				<LinkButton header label="Interest List" icon="list_alt" href="/interests" />
				<LinkButton header label="Scavenger Hunt" icon="travel_explore" href="/scavenger-hunt" />
			</div>
			<div class="menuBottom">
				<ThemeSwitcher header />
				<LinkButton headerSmall label="Settings" icon="settings" href="/settings" />
				<LinkButton headerSmall label="App feedback" icon="message" href="/feedback" />
				<LinkButton headerSmall label="Fair sponsors" icon="monetization_on" href="/sponsors" />
				<LinkButton headerSmall label="About 4-H" href="https://4histops.org">
					<svelte:fragment slot="iconElement">
						<FourH
							style="height: 100%; fill: currentColor; transition: fill var(--theme-transition);"
						/>
					</svelte:fragment>
				</LinkButton>
			</div>
			<div class="dqpmdptSpot">
				<SponsorSpot />
			</div>
		</div>
	</div>
</div>

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

		& > :global(svg) {
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
		/* cursor: pointer; */
		/* user-select: none; */
		/* box-shadow: 0 0 6px 0px #0008; */
		/* -webkit-tap-highlight-color: rgba(0, 0, 0, 0); */
		/* transition: (filter, transform) 120ms ease; */

		&:focus {
			outline: none;
		}

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
