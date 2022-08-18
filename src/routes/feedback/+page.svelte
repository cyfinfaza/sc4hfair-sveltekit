<script>
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { session, initSupabaseClient } from 'logic/supabase.js';
	import { onMount } from 'svelte';

	let errorText = '',
		formSubmitted = false,
		name,
		email,
		comment;

	onMount(initSupabaseClient);
	let formPrefilled = false;
	$: if (!formPrefilled && $session?.user?.user_metadata) {
		formPrefilled = true;
		if (!name) name = $session.user.user_metadata.fullName;
		if (!email) email = $session.user.user_metadata.preferredEmail || $session.user.user_metadata.email;
	}

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
		formData.append('entry.118251261', `${__COMMIT__}/${__BRANCH__}`);
		formData.append('entry.87818926', navigator.userAgent);

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
		<p placeholder="Type your name here" contenteditable bind:textContent={name} />
		<h2>Email</h2>
		<p placeholder="Type your email here" contenteditable bind:textContent={email} />
		<h2>Comment<span>*</span></h2>
		<p placeholder="Type your comment here" contenteditable bind:textContent={comment} />
		<p style:color="red">{errorText}</p>
		<LinkButton label="Submit" icon="send" on:click={submit} />
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
