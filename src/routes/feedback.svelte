<script>
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';

	let errorText = '',
		formSubmitted = false,
		name,
		email,
		comment;

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
		formData.append('entry.118251261', __VERSION__);
		formData.append('entry.87818926', navigator.userAgent);

		fetch(
			'https://docs.google.com/forms/u/0/d/e/1FAIpQLSeCrjrBodgfkJ1vFL5-fJl3k1RBx01jiF5w5V49Chc6uO_S5w/formResponse',
			{
				body: formData,
				method: 'post',
				mode: 'no-cors',
			}
		).then((response) => {
			// console.log(response)
			name = '';
			email = '';
			comment = '';
			formSubmitted = true;
		});
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

<style>
	p[contenteditable]:empty::before {
		opacity: 0.5;
		content: attr(placeholder);
	}
	p[contenteditable]:is(:focus, :active) {
		outline: none;
		border-bottom-color: var(--accent);
	}
	p[contenteditable] {
		cursor: text;
		border: none;
		border-bottom: solid 2px var(--light-translucent);
		transition: 60ms;
	}
	h2 span {
		color: red;
		opacity: 0.75;
		padding-left: 0.05em;
	}
</style>
