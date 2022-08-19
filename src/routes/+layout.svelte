<script>
	import { setContext } from 'svelte';

	import 'styles/global.css';
	import 'styles/material-icons.css';
	import 'styles/fonts.css';

	export let data;
	setContext('sponsors', data?.sponsors || []);
</script>

<slot />
