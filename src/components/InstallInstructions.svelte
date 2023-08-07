<script>
	import { browser } from '$app/environment';
	import { getPlatform } from 'logic/platform.js';
	const platform = getPlatform();
</script>

{#if platform === 'android'}
	<ol>
		<li>
			Look for and follow the prompt asking you to install or add this app to your home screen
			(usually at the bottom)
		</li>
		<li>
			If you don't see it, tap <span class="material-icons" aria-hidden="true">more_vert</span> (menu),
			then tap "Add to Home Screen" or "Install".
		</li>
	</ol>
{:else if platform === 'android-unsupported'}
	<p>
		First open this site {#if browser}
			(<a href={window.location.origin}>{window.location.origin}</a>){' '}
		{/if}in Chrome or another web browser app.
	</p>
{:else if platform === 'ios-unsupported'}
	<p>
		First open this site {#if browser}
			(<a href={window.location.origin}>{window.location.origin}</a>){' '}
		{/if}in Safari.
	</p>
{:else if platform === 'ios' || platform === 'ios-other'}
	{#if platform === 'ios-other'}<small>
			Note: Adding apps to the home screen in browsers other than Safari is a new feature and may
			not be supported on all iPhones.
		</small>{/if}
	<ol>
		<li>
			Tap <span class="material-icons" aria-hidden="true">ios_share</span>
			(share button{#if platform === 'ios-other'}, which may be inside another menu{/if})
		</li>
		<li>
			Scroll down until you see "Add to Home Screen
			<span class="material-icons" aria-hidden="true">add_box</span>" and click it{#if platform === 'ios-other'}.
				If you don't see the option, try opening this site
				{#if browser}(<a href={window.location.origin}>{window.location.origin}</a>){' '}{/if}in
				Safari.{/if}
		</li>
		<li>Tap "Add" in the upper right corner</li>
	</ol>
	<small>
		Note: On iPhone you are required to add the app to your homescreen before enabling
		notifications.
	</small>
{:else if platform === 'other'}
	<p>
		Look for a prompt asking you to install, create a shortcut, or add this app to your home screen.
		If you don't see it, you might have to open a menu and find the option, or your browser might
		not support this feature.
	</p>
{/if}
