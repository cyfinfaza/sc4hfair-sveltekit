<script>
	import '../styles/button.css';
	import LinkButton from './LinkButton.svelte';
	import Logo from '../assets/logo.inline.svg';
	import { menuOpen, isOnline } from '../logic/stores';
	export let offsetContent = false;
</script>

<div class="invisible">
	<div
		class="visible"
		style:height={$menuOpen ? '100vh' : ''}
		style:background={$isOnline ? 'var(--navbar)' : 'var(--navbar-grey)'}
	>
		<div class="topBar">
			<Logo
				class="logo"
				role="button"
				onclick="window.location.href = '/'"
				style="cursor: pointer; fill: currentColor;"
			/>
			<div class="horizPanel2" style:gap="12px">
				{#if !$isOnline}
					<span class="material-icons">cloud_off</span>
				{/if}
				<button class="menuButton button" on:click={(_) => ($menuOpen = !$menuOpen)}>
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
				<LinkButton header label="Latest" icon="home" href="/" opaque={false} />
				<LinkButton header label="Schedule" icon="event_note" href="/schedule" opaque={false} />
				<LinkButton header label="Clubs" icon="groups" href="/clubs" opaque={false} />
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

		> * {
			white-space: nowrap;
		}
	}

	.headerLogo {
		height: 100%;
		/* fill: var(--navbar-text); */
		fill: var(--text);
		transition: fill var(--theme-transition);
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

	.sponsorArea {
		width: 100%;
		max-width: 500px;
		box-sizing: border-box;
		--spsp-bg: var(--navbar-accent);
	}
</style>
