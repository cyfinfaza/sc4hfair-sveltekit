<script>
	import Logo from 'assets/logo.svg?component';
	import LinkButton from 'components/LinkButton.svelte';
	import { page, navigating } from '$app/stores';
	import LoadingRing from 'components/LoadingRing.svelte';

	const links = [
		{
			name: 'Map',
			path: '/map',
			icon: 'map',
			description: 'Explore an interactive map of the fair and see what clubs are in each tent.',
		},
		{
			name: 'Schedule',
			path: '/schedule',
			icon: 'event_note',
			description:
				"Find out what's happening at the fair, where it's happening, and who's hosting it.",
		},
		{
			name: 'Food',
			path: '/food',
			icon: 'fastfood',
			description:
				'Browse the menu of food options available at the fair from vendors in the food tent.',
		},
		{
			name: 'Clubs',
			path: '/clubs',
			icon: 'groups',
			description: "See a list of all the clubs at the fair and find out what tent they're in",
		},
		{
			name: 'Announcements',
			path: '/?km_announcements=true',
			match: '/',
			icon: 'notifications',
			description: 'See latest updates from the 4-H Fair managers.',
		},
		{
			name: 'Get the App!',
			path: '/get-the-app',
			icon: 'smartphone',
			description: 'Take this interactive experience with you around the fair.',
		},
	];
</script>

<div class="kioskMenu">
	<div>
		<div
			style="position: fixed; top:0.5em; left:0.5em; display: flex; align-items: center; justify-content: center; width: 2em; height 2em;"
		>
			<LoadingRing loading={$navigating} />
		</div>
		<a
			href="/"
			aria-label="Main page"
			data-sveltekit-reload={true}
			onclick="window.location.href = '/';"
		>
			<Logo />
		</a>
		<h3 style="text-align: center;">Welcome to the 4-H Fair! <br /> Select a screen below:</h3>
		<!-- <h1>Welcome!</h1> -->
		{#each links as link}
			<a
				href={link.path}
				class="bigLinkButton button"
				class:activePage={$page.url.pathname == (link.match || link.path)}
			>
				<span class="material-icons icon" aria-hidden="true">{link.icon}</span>
				<div>
					<h2>{link.name}</h2>
					<p style="font-size: 0.8em;">{link.description}</p>
				</div>
			</a>
		{/each}
	</div>
	<div>
		<!-- <LinkButton headerSmall icon="settings" href="/settings" /> -->
	</div>
</div>

<style lang="scss">
	.kioskMenu {
		height: 100%;
		width: 100%;
		font-size: 1em;
		padding: 1em;
		box-sizing: border-box;
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-direction: column;
		background: var(--navbar);
		gap: 1em;
		box-shadow: 0 0 8px 0px #0008;
		// border-right: 3px solid var(--text);
		// overflow-x: hidden;
		overflow-y: auto;
		> div {
			display: flex;
			flex-direction: column;
			gap: inherit;
			align-items: center;
		}
		* {
			margin: 0;
		}
		:global(svg) {
			height: 2em;
			fill: currentColor;
			transition: fill var(--theme-transition);
			cursor: pointer;
		}
	}
	.bigLinkButton {
		text-decoration: none;
		display: flex;
		align-items: center;
		gap: 0.75em;
		min-height: 6em;
		background-color: var(--navbar-accent);
		border-radius: 1em;
		padding: 0.75em;
		transition: 240ms;
		width: 100%;
		box-sizing: border-box;
		border: 3px solid transparent;
		.icon {
			font-size: 3em;
		}
		* {
			margin: 0;
		}
		&.activePage {
			border: 3px solid var(--text);
			box-shadow: 0 0 8px 0px var(--text);
			// border-right: 3px solid var(--bg);
			// transform: translateX(calc(1em + 3px));
			// border-top-right-radius: 0;
			// border-bottom-right-radius: 0;
			// background: var(--bg);
		}
	}
	:global(:root:has(.kioskMenu)) {
		--nav-height: 0;
		&,
		* {
			&::-webkit-scrollbar {
				width: 0;
			}
		}
	}
</style>
