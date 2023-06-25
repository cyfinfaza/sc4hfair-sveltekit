<script>
	import { browser, dev, version } from '$app/environment';
	import { goto } from '$app/navigation';
	import { writable } from 'svelte/store';
	import { isStandalone } from 'logic/platform.js';
	import { isOnline } from 'logic/stores.js';
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import LabeledInput from 'components/LabeledInput.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Modal from 'components/Modal.svelte';
	import NoOffline from 'components/NoOffline.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	import { onMount } from 'svelte';
	import { session, initSupabaseClient, logout, interestsSlugs } from 'logic/supabase.js';
	import { getSubscription, subscribe, unsubscribe } from 'logic/webpush';
	import NotificationEnableButton from 'components/NotificationEnableButton.svelte';

	function isInfoFormDisabled(a, b) {
		if (!a || !b) return true;
		// only check certain properties
		return ['fullName', 'preferredEmail', 'phone', 'graduation'].every((key) => a[key] === b[key]);
		// return JSON.stringify(a) === JSON.stringify(b)
	}
	const form = writable({
		fullName: '',
		preferredEmail: '',
		phone: '',
		graduation: '',
	});
	let cloudForm;
	// $: console.log($form, cloudForm);
	// $: console.log($session);

	/** @type {import('@supabase/supabase-js').SupabaseClient} */
	let client;

	let confirmReset = ''; // modal for confirmation

	let showingAdditionalBuildInfo = dev;

	onMount(async () => {
		client = await initSupabaseClient();
	});

	$: {
		(function (s) {
			if (client && s) {
				cloudForm = s.user?.user_metadata || {};
				console.log('new cloud user metadata', cloudForm);
				$form = { ...cloudForm };
			}
		})($session);
	}
</script>

<Layout title="Settings">
	<h1>Account</h1>
	{#if $session}
		<p>You are signed in as <strong>{$session?.user?.email}</strong></p>
		<p>
			<LinkButton label="Sign out" icon="logout" on:click={() => logout()} />
		</p>
		<h2>
			Additional information <small>(optional)</small>
		</h2>
		<table style="width: 100%; margin: 1rem 0;">
			<tbody>
				<LabeledInput {form} name="fullName" label="Full name" />
				<LabeledInput {form} name="preferredEmail" label="Preferred email" type="email" />
				<LabeledInput {form} name="phone" label="Phone number" type="tel" />
				<LabeledInput
					{form}
					name="graduation"
					label="Graduation year"
					type="number"
					min="1900"
					max="2099"
					step="1"
				/>
			</tbody>
		</table>
		<LinkButton
			label="Save"
			icon="save"
			on:click={() => {
				client.auth.updateUser({ data: $form });
				cloudForm = { ...$form };
			}}
			disabled={isInfoFormDisabled($form, cloudForm) || !$isOnline}
			alert={!isInfoFormDisabled($form, cloudForm)}
		/>
	{:else if !$isOnline}
		<NoOffline />
	{:else}
		<SignInButtons redirect="/settings" />
	{/if}

	<h1>Add to homescreen</h1>
	{#if $isStandalone}
		<p>This site is already running in standalone mode.</p>
	{:else}
		<p>To add the fair app to your homescreen:</p>
		<InstallInstructions />
	{/if}

	<h1 id="notifications">Notifications</h1>
	<NotificationEnableButton />

	<h1>Clear data</h1>
	<p class="horizPanel2">
		<LinkButton
			label="Reset Scavenger Hunt"
			on:click={() => (confirmReset = 'sh')}
			icon="restart_alt"
		/>
		{#if $session}
			<LinkButton
				label="Clear Interest List"
				on:click={() => (confirmReset = 'interests')}
				icon="clear_all"
			/>
		{/if}
	</p>
	<Modal
		show={!!confirmReset}
		danger
		on:close={() => (confirmReset = '')}
		on:confirm={async () => {
			switch (confirmReset) {
				case 'sh':
					localStorage.removeItem('sh_code');
					localStorage.removeItem('sh_hints');
					goto('/scavenger-hunt');
					break;
				case 'interests':
					localStorage.removeItem('cim_intent');
					if (client) {
						const { error } = await client
							.from('interests')
							.delete()
							.match({ owner: $session.user.id });
						if (error) alert(error.message);
						else interestsSlugs.update(() => []);
					}
					goto('/interests');
					break;
			}
		}}
	>
		<p>
			Are you sure you want to reset {confirmReset === 'sh'
				? 'your scavenger hunt progress'
				: 'this'}? You will not be able to restore it.
		</p>
		{#if confirmReset === 'sh'}
			<p>Note that you may only claim one prize per person.</p>
		{/if}
	</Modal>

	<h1>About</h1>
	<p>
		This app was created by the
		<a href="https://4hcomputers.club">Somerset County 4-H Computer Club</a>.
	</p>
	<p class="horizPanel2">
		<LinkButton label="Send feedback" disabled={!$isOnline} href="/feedback" icon="message" />
		<LinkButton label="Privacy Policy" href="/privacy-policy" icon="policy" />
	</p>
	<div style:opacity={0.5}>
		<code
			role="button"
			tabindex="0"
			on:click={() => (showingAdditionalBuildInfo = !showingAdditionalBuildInfo)}
			on:keydown={(e) =>
				e.key === 'Enter' && (showingAdditionalBuildInfo = !showingAdditionalBuildInfo)}
			style:cursor="pointer"
		>
			{version}
		</code>
		{#if showingAdditionalBuildInfo && browser}
			<br />
			<!-- svelte-ignore missing-declaration -->
			<code>{__BRANCH__}</code>
			<br />
			<!-- svelte-ignore missing-declaration -->
			<code>{__BUILD_TIME__}</code>
			<br />
			<!-- svelte-ignore missing-declaration -->
			<code>{__BUILD_LOCATION__}</code>
			<div class="horizPanel2">
				<LinkButton
					icon="settings_suggest"
					label="Unregister service worker"
					on:click={() => {
						navigator.serviceWorker.getRegistrations().then(function (registrations) {
							for (let registration of registrations) {
								registration.unregister();
							}
						});
					}}
				/>
				<LinkButton
					icon="update"
					label="Check for update (sw)"
					on:click={async () => {
						const swRegistration = await navigator.serviceWorker.getRegistration();
						swRegistration?.update();
					}}
				/>
				<LinkButton
					icon="cleaning_services"
					label="Remove localStorage item"
					on:click={() => {
						localStorage.removeItem(prompt('Key:'));
					}}
				/>
				<LinkButton
					icon="autorenew"
					label="Clear caches"
					on:click={() => {
						window.caches.keys().then(function (keys) {
							for (let key of keys) {
								window.caches.delete(key);
							}
						});
					}}
				/>
			</div>
			<hr />
			<div class="horizPanel2">
				<LinkButton
					icon="notifications_active"
					label="Test notification"
					on:click={async () => {
						new window.Notification('Fair Update', {
							body: 'The fair has been closed due to test weather.',
						});
					}}
				/>
				<LinkButton
					icon="notifications"
					label="Get notification subscription"
					on:click={async () => {
						console.log('getting subscription');
						const sub = await getSubscription();
						alert(JSON.stringify(sub));
						console.log(JSON.stringify(sub));
						console.log('got subscription');
					}}
				/>
				<LinkButton
					icon="notification_add"
					label="Subscribe to notifications"
					on:click={async () => {
						console.log((await subscribe()).registered);
					}}
				/>
				<LinkButton
					icon="notifications_off"
					label="Unubscribe from notifications"
					on:click={async () => {
						console.log(!(await unsubscribe()).registered);
					}}
				/>
			</div>
		{/if}
	</div>
</Layout>
