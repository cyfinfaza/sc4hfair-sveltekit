<script lang="ts">
	import { version } from '$app/environment';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { session, getProfile } from 'logic/auth';
	import { BRANCH } from 'logic/constants';
	import { isOnline } from 'logic/stores.svelte';

	let errorText = $state(''),
		formPrefilled = $state(false),
		formSubmitted = $state(false),
		name: string = $state(''),
		email: string = $state(''),
		comment: string = $state('');

	async function prefillForm() {
		if (!formPrefilled) {
			formPrefilled = true;
			const profile = await getProfile();
			if (!name) name = profile?.name;
			if (!email) email = profile?.preferredEmail || $session?.email;
		}
	}
	$effect(() => {
		if (!formPrefilled && $session) prefillForm();
	});

	function submit() {
		if (!comment) {
			errorText = 'You must input a comment.';
			return;
		}
		if (!name) {
			errorText = 'You must input a name so the app committee can identify you.';
			return;
		}

		let formData = new FormData();
		formData.append('entry.1901667750', name);
		formData.append('entry.614631811', email);
		formData.append('entry.1550740052', comment);
		formData.append('entry.118251261', `${version}/${BRANCH}`);
		formData.append('entry.87818926', navigator.userAgent);
		// todo: if form integration broke send directly to discord?

		fetch(
			'https://docs.google.com/forms/u/0/d/e/1FAIpQLSeCrjrBodgfkJ1vFL5-fJl3k1RBx01jiF5w5V49Chc6uO_S5w/formResponse',
			{
				body: formData,
				method: 'post',
				mode: 'no-cors',
			}
		).then(() => (formSubmitted = true));
	}
</script>

<Layout title="Feedback">
	{#if formSubmitted}
		<p>Thank you for your feedback!</p>
	{:else}
		<h2>Name<span>*</span></h2>
		<p placeholder="Type your name here" contenteditable bind:textContent={name}></p>
		<h2>Email</h2>
		<p placeholder="Type your email here" contenteditable bind:textContent={email}></p>
		<h2>Comment<span>*</span></h2>
		<p placeholder="Type your comment here" contenteditable bind:textContent={comment}></p>
		<p style:color="red">{errorText}</p>
		<LinkButton label="Submit" icon="send" onclick={submit} disabled={!$isOnline} />
	{/if}
</Layout>

<style lang="scss">
	p[contenteditable] {
		cursor: text;
		border: none;
		border-bottom: solid 2px var(--light-translucent);
		transition: 60ms;

		&:empty::before {
			opacity: 0.5;
			content: attr(placeholder);
		}
		&:focus,
		&:active {
			outline: none;
			border-bottom-color: var(--accent);
		}
	}
	h2 span {
		color: red;
		opacity: 0.75;
		padding-left: 0.05em;
	}
</style>
