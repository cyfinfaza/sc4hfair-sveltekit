<script>
	import { browser } from '$app/env';
	import { goto } from '$app/navigation';
	import { writable } from 'svelte/store';
	import { isStandalone } from 'logic/platform.js';
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import LabeledInput from 'components/LabeledInput.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Modal from 'components/Modal.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	import { onMount } from 'svelte';
	import { session, initSupabaseClient, logout } from 'logic/supabase.js';

	function isInfoFormDisabled(a, b) {
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
	let cloudForm = form; // @todo: add cloud functionality
	$: console.log($form, cloudForm);
	$: console.log(isInfoFormDisabled($form, cloudForm));
	$: console.log($session);

	let client;

	let confirmReset = ''; // @todo: modal for confirmation

	let showingAdditionalBuildInfo = false;

	onMount(async (_) => {
		client = await initSupabaseClient();
	});

	$: {
		(function (s) {
			if (s) {
				cloudForm = s.user.user_metadata;
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
		<table style={{ width: '100%', margin: '1rem 0' }}>
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
				client.auth.update({ data: $form });
				cloudForm = { ...$form };
			}}
			disabled={isInfoFormDisabled($form, cloudForm)}
			alert={!isInfoFormDisabled($form, cloudForm)}
		/>
	{:else}
		<SignInButtons />
	{/if}

	<h1>Install as app</h1>
	{#if browser && isStandalone()}
		<p>This site is already installed as an app.</p>
	{:else}
		<p>This site is not installed as an app, to do so:</p>
		<InstallInstructions />
	{/if}

	<h1>Clear data</h1>
	<p class="horizPanel2">
		<LinkButton
			label="Reset Scavenger Hunt"
			on:click={() => (confirmReset = 'sh')}
			icon="restart_alt"
		/>
	</p>
	<Modal
		show={!!confirmReset}
		confirmation={true}
		on:close={() => (confirmReset = '')}
		on:confirm={() => {
			switch (confirmReset) {
				case 'sh':
					localStorage.removeItem('sh_code');
					localStorage.removeItem('sh_hints');
					goto('/scavenger-hunt');
					break;
				default:
					confirmReset = '';
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
		This app was created by the <a href="https://4hcomputers.club"
			>Somerset County 4-H Computer Club</a
		>.
	</p>
	<p class="horizPanel2">
		<LinkButton label="Send feedback" href="/feedback" icon="message" />
		<LinkButton label="Privacy Policy" href="/privacy-policy" icon="policy" />
	</p>
	<div style:opacity={0.5}>
		<!-- svelte-ignore missing-declaration -->
		<code
			role="button"
			tabIndex={0}
			on:click={() => (showingAdditionalBuildInfo = true)}
			on:keydown={() => (showingAdditionalBuildInfo = true)}
			style:cursor={showingAdditionalBuildInfo ? null : 'pointer'}
		>
			{__COMMIT__}/{__BRANCH__}
		</code>
		{#if showingAdditionalBuildInfo && browser}
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
		{/if}
	</div>
</Layout>
