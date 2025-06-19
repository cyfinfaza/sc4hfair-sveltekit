<script lang="ts">
	let {
		name,
		label,
		type = 'text',
		form,
		...rest
	}: {
		name: string;
		label: string;
		type?: string;
		form: import('svelte/store').Writable<Record<string, any>>;
		[key: string]: any;
	} = $props();

	const typeAction: import('svelte/action').Action<HTMLInputElement> = (node) => {
		node.type = type;
	};
</script>

<tr>
	<td>
		<label for={name}>{label}</label>
	</td>
	<td>
		<input use:typeAction {name} bind:value={$form[name]} {...rest} />
	</td>
</tr>
