<script>
	export let name; // internal id
	export let label; // displayed text
	export let type = 'text'; // input type
	export let form; // form writeable

	function typeAction(node) {
		node.type = type;
	}
</script>

<tr>
	<td>
		<label for={name}>{label}</label>
	</td>
	<td>
		<input use:typeAction {name} bind:value={$form[name]} {...$$restProps} />
	</td>
</tr>
