<script>
	export let box = true;
	export let title = undefined;
</script>

<div class:installBox={box} class:center={box}>
	{#if box}<h2>{title || 'This feature is available in the app.'}</h2>{/if}
	{#if $$slots.default}
		<slot />
	{:else}
		<p>Get it on your device for a better experience as you navigate the fair.</p>
	{/if}

	<svg
		width="200px"
		viewBox="80 80 580 580"
		shape-rendering="crispEdges"
		style="fill: currentColor; margin: 0 auto;"
	>
		<rect x="240" y="80" width="20" height="20" />
		<rect x="260" y="80" width="20" height="20" />
		<rect x="280" y="80" width="20" height="20" />
		<rect x="320" y="80" width="20" height="20" />
		<rect x="340" y="80" width="20" height="20" />
		<rect x="380" y="80" width="20" height="20" />
		<rect x="260" y="100" width="20" height="20" />
		<rect x="320" y="100" width="20" height="20" />
		<rect x="400" y="100" width="20" height="20" />
		<rect x="420" y="100" width="20" height="20" />
		<rect x="440" y="100" width="20" height="20" />
		<rect x="480" y="100" width="20" height="20" />
		<rect x="300" y="120" width="20" height="20" />
		<rect x="320" y="120" width="20" height="20" />
		<rect x="340" y="120" width="20" height="20" />
		<rect x="440" y="120" width="20" height="20" />
		<rect x="460" y="120" width="20" height="20" />
		<rect x="240" y="140" width="20" height="20" />
		<rect x="300" y="140" width="20" height="20" />
		<rect x="320" y="140" width="20" height="20" />
		<rect x="340" y="140" width="20" height="20" />
		<rect x="380" y="140" width="20" height="20" />
		<rect x="440" y="140" width="20" height="20" />
		<rect x="240" y="160" width="20" height="20" />
		<rect x="260" y="160" width="20" height="20" />
		<rect x="280" y="160" width="20" height="20" />
		<rect x="340" y="160" width="20" height="20" />
		<rect x="380" y="160" width="20" height="20" />
		<rect x="400" y="160" width="20" height="20" />
		<rect x="460" y="160" width="20" height="20" />
		<rect x="480" y="160" width="20" height="20" />
		<rect x="240" y="180" width="20" height="20" />
		<rect x="260" y="180" width="20" height="20" />
		<rect x="280" y="180" width="20" height="20" />
		<rect x="320" y="180" width="20" height="20" />
		<rect x="340" y="180" width="20" height="20" />
		<rect x="360" y="180" width="20" height="20" />
		<rect x="380" y="180" width="20" height="20" />
		<rect x="420" y="180" width="20" height="20" />
		<rect x="460" y="180" width="20" height="20" />
		<rect x="240" y="200" width="20" height="20" />
		<rect x="280" y="200" width="20" height="20" />
		<rect x="320" y="200" width="20" height="20" />
		<rect x="360" y="200" width="20" height="20" />
		<rect x="400" y="200" width="20" height="20" />
		<rect x="440" y="200" width="20" height="20" />
		<rect x="480" y="200" width="20" height="20" />
		<rect x="240" y="220" width="20" height="20" />
		<rect x="260" y="220" width="20" height="20" />
		<rect x="320" y="220" width="20" height="20" />
		<rect x="420" y="220" width="20" height="20" />
		<rect x="440" y="220" width="20" height="20" />
		<rect x="460" y="220" width="20" height="20" />
		<rect x="480" y="220" width="20" height="20" />
		<rect x="80" y="240" width="20" height="20" />
		<rect x="160" y="240" width="20" height="20" />
		<rect x="200" y="240" width="20" height="20" />
		<rect x="220" y="240" width="20" height="20" />
		<rect x="240" y="240" width="20" height="20" />
		<rect x="260" y="240" width="20" height="20" />
		<rect x="320" y="240" width="20" height="20" />
		<rect x="340" y="240" width="20" height="20" />
		<rect x="360" y="240" width="20" height="20" />
		<rect x="400" y="240" width="20" height="20" />
		<rect x="420" y="240" width="20" height="20" />
		<rect x="440" y="240" width="20" height="20" />
		<rect x="460" y="240" width="20" height="20" />
		<rect x="480" y="240" width="20" height="20" />
		<rect x="500" y="240" width="20" height="20" />
		<rect x="520" y="240" width="20" height="20" />
		<rect x="540" y="240" width="20" height="20" />
		<rect x="560" y="240" width="20" height="20" />
		<rect x="580" y="240" width="20" height="20" />
		<rect x="640" y="240" width="20" height="20" />
		<rect x="80" y="260" width="20" height="20" />
		<rect x="120" y="260" width="20" height="20" />
		<rect x="140" y="260" width="20" height="20" />
		<rect x="160" y="260" width="20" height="20" />
		<rect x="220" y="260" width="20" height="20" />
		<rect x="300" y="260" width="20" height="20" />
		<rect x="360" y="260" width="20" height="20" />
		<rect x="440" y="260" width="20" height="20" />
		<rect x="460" y="260" width="20" height="20" />
		<rect x="480" y="260" width="20" height="20" />
		<rect x="540" y="260" width="20" height="20" />
		<rect x="560" y="260" width="20" height="20" />
		<rect x="600" y="260" width="20" height="20" />
		<rect x="80" y="280" width="20" height="20" />
		<rect x="100" y="280" width="20" height="20" />
		<rect x="120" y="280" width="20" height="20" />
		<rect x="140" y="280" width="20" height="20" />
		<rect x="180" y="280" width="20" height="20" />
		<rect x="200" y="280" width="20" height="20" />
		<rect x="240" y="280" width="20" height="20" />
		<rect x="280" y="280" width="20" height="20" />
		<rect x="300" y="280" width="20" height="20" />
		<rect x="320" y="280" width="20" height="20" />
		<rect x="340" y="280" width="20" height="20" />
		<rect x="360" y="280" width="20" height="20" />
		<rect x="400" y="280" width="20" height="20" />
		<rect x="440" y="280" width="20" height="20" />
		<rect x="480" y="280" width="20" height="20" />
		<rect x="520" y="280" width="20" height="20" />
		<rect x="560" y="280" width="20" height="20" />
		<rect x="580" y="280" width="20" height="20" />
		<rect x="600" y="280" width="20" height="20" />
		<rect x="640" y="280" width="20" height="20" />
		<rect x="100" y="300" width="20" height="20" />
		<rect x="120" y="300" width="20" height="20" />
		<rect x="160" y="300" width="20" height="20" />
		<rect x="260" y="300" width="20" height="20" />
		<rect x="280" y="300" width="20" height="20" />
		<rect x="300" y="300" width="20" height="20" />
		<rect x="320" y="300" width="20" height="20" />
		<rect x="340" y="300" width="20" height="20" />
		<rect x="420" y="300" width="20" height="20" />
		<rect x="460" y="300" width="20" height="20" />
		<rect x="480" y="300" width="20" height="20" />
		<rect x="500" y="300" width="20" height="20" />
		<rect x="540" y="300" width="20" height="20" />
		<rect x="580" y="300" width="20" height="20" />
		<rect x="80" y="320" width="20" height="20" />
		<rect x="100" y="320" width="20" height="20" />
		<rect x="140" y="320" width="20" height="20" />
		<rect x="160" y="320" width="20" height="20" />
		<rect x="180" y="320" width="20" height="20" />
		<rect x="200" y="320" width="20" height="20" />
		<rect x="240" y="320" width="20" height="20" />
		<rect x="280" y="320" width="20" height="20" />
		<rect x="320" y="320" width="20" height="20" />
		<rect x="340" y="320" width="20" height="20" />
		<rect x="400" y="320" width="20" height="20" />
		<rect x="460" y="320" width="20" height="20" />
		<rect x="520" y="320" width="20" height="20" />
		<rect x="540" y="320" width="20" height="20" />
		<rect x="580" y="320" width="20" height="20" />
		<rect x="600" y="320" width="20" height="20" />
		<rect x="620" y="320" width="20" height="20" />
		<rect x="80" y="340" width="20" height="20" />
		<rect x="100" y="340" width="20" height="20" />
		<rect x="160" y="340" width="20" height="20" />
		<rect x="180" y="340" width="20" height="20" />
		<rect x="220" y="340" width="20" height="20" />
		<rect x="260" y="340" width="20" height="20" />
		<rect x="300" y="340" width="20" height="20" />
		<rect x="340" y="340" width="20" height="20" />
		<rect x="360" y="340" width="20" height="20" />
		<rect x="380" y="340" width="20" height="20" />
		<rect x="460" y="340" width="20" height="20" />
		<rect x="480" y="340" width="20" height="20" />
		<rect x="560" y="340" width="20" height="20" />
		<rect x="600" y="340" width="20" height="20" />
		<rect x="100" y="360" width="20" height="20" />
		<rect x="120" y="360" width="20" height="20" />
		<rect x="140" y="360" width="20" height="20" />
		<rect x="160" y="360" width="20" height="20" />
		<rect x="200" y="360" width="20" height="20" />
		<rect x="280" y="360" width="20" height="20" />
		<rect x="300" y="360" width="20" height="20" />
		<rect x="320" y="360" width="20" height="20" />
		<rect x="400" y="360" width="20" height="20" />
		<rect x="440" y="360" width="20" height="20" />
		<rect x="520" y="360" width="20" height="20" />
		<rect x="540" y="360" width="20" height="20" />
		<rect x="560" y="360" width="20" height="20" />
		<rect x="580" y="360" width="20" height="20" />
		<rect x="600" y="360" width="20" height="20" />
		<rect x="620" y="360" width="20" height="20" />
		<rect x="120" y="380" width="20" height="20" />
		<rect x="240" y="380" width="20" height="20" />
		<rect x="260" y="380" width="20" height="20" />
		<rect x="360" y="380" width="20" height="20" />
		<rect x="420" y="380" width="20" height="20" />
		<rect x="460" y="380" width="20" height="20" />
		<rect x="480" y="380" width="20" height="20" />
		<rect x="500" y="380" width="20" height="20" />
		<rect x="620" y="380" width="20" height="20" />
		<rect x="100" y="400" width="20" height="20" />
		<rect x="120" y="400" width="20" height="20" />
		<rect x="180" y="400" width="20" height="20" />
		<rect x="200" y="400" width="20" height="20" />
		<rect x="220" y="400" width="20" height="20" />
		<rect x="240" y="400" width="20" height="20" />
		<rect x="320" y="400" width="20" height="20" />
		<rect x="340" y="400" width="20" height="20" />
		<rect x="360" y="400" width="20" height="20" />
		<rect x="400" y="400" width="20" height="20" />
		<rect x="420" y="400" width="20" height="20" />
		<rect x="460" y="400" width="20" height="20" />
		<rect x="480" y="400" width="20" height="20" />
		<rect x="500" y="400" width="20" height="20" />
		<rect x="540" y="400" width="20" height="20" />
		<rect x="580" y="400" width="20" height="20" />
		<rect x="600" y="400" width="20" height="20" />
		<rect x="620" y="400" width="20" height="20" />
		<rect x="80" y="420" width="20" height="20" />
		<rect x="120" y="420" width="20" height="20" />
		<rect x="160" y="420" width="20" height="20" />
		<rect x="180" y="420" width="20" height="20" />
		<rect x="220" y="420" width="20" height="20" />
		<rect x="260" y="420" width="20" height="20" />
		<rect x="320" y="420" width="20" height="20" />
		<rect x="400" y="420" width="20" height="20" />
		<rect x="440" y="420" width="20" height="20" />
		<rect x="520" y="420" width="20" height="20" />
		<rect x="560" y="420" width="20" height="20" />
		<rect x="600" y="420" width="20" height="20" />
		<rect x="120" y="440" width="20" height="20" />
		<rect x="140" y="440" width="20" height="20" />
		<rect x="180" y="440" width="20" height="20" />
		<rect x="200" y="440" width="20" height="20" />
		<rect x="260" y="440" width="20" height="20" />
		<rect x="280" y="440" width="20" height="20" />
		<rect x="300" y="440" width="20" height="20" />
		<rect x="340" y="440" width="20" height="20" />
		<rect x="360" y="440" width="20" height="20" />
		<rect x="440" y="440" width="20" height="20" />
		<rect x="460" y="440" width="20" height="20" />
		<rect x="520" y="440" width="20" height="20" />
		<rect x="560" y="440" width="20" height="20" />
		<rect x="580" y="440" width="20" height="20" />
		<rect x="600" y="440" width="20" height="20" />
		<rect x="640" y="440" width="20" height="20" />
		<rect x="160" y="460" width="20" height="20" />
		<rect x="260" y="460" width="20" height="20" />
		<rect x="340" y="460" width="20" height="20" />
		<rect x="400" y="460" width="20" height="20" />
		<rect x="420" y="460" width="20" height="20" />
		<rect x="460" y="460" width="20" height="20" />
		<rect x="500" y="460" width="20" height="20" />
		<rect x="620" y="460" width="20" height="20" />
		<rect x="80" y="480" width="20" height="20" />
		<rect x="100" y="480" width="20" height="20" />
		<rect x="160" y="480" width="20" height="20" />
		<rect x="200" y="480" width="20" height="20" />
		<rect x="240" y="480" width="20" height="20" />
		<rect x="260" y="480" width="20" height="20" />
		<rect x="280" y="480" width="20" height="20" />
		<rect x="320" y="480" width="20" height="20" />
		<rect x="340" y="480" width="20" height="20" />
		<rect x="460" y="480" width="20" height="20" />
		<rect x="480" y="480" width="20" height="20" />
		<rect x="500" y="480" width="20" height="20" />
		<rect x="520" y="480" width="20" height="20" />
		<rect x="540" y="480" width="20" height="20" />
		<rect x="560" y="480" width="20" height="20" />
		<rect x="240" y="500" width="20" height="20" />
		<rect x="260" y="500" width="20" height="20" />
		<rect x="340" y="500" width="20" height="20" />
		<rect x="360" y="500" width="20" height="20" />
		<rect x="380" y="500" width="20" height="20" />
		<rect x="460" y="500" width="20" height="20" />
		<rect x="480" y="500" width="20" height="20" />
		<rect x="560" y="500" width="20" height="20" />
		<rect x="580" y="500" width="20" height="20" />
		<rect x="600" y="500" width="20" height="20" />
		<rect x="240" y="520" width="20" height="20" />
		<rect x="280" y="520" width="20" height="20" />
		<rect x="300" y="520" width="20" height="20" />
		<rect x="380" y="520" width="20" height="20" />
		<rect x="440" y="520" width="20" height="20" />
		<rect x="460" y="520" width="20" height="20" />
		<rect x="480" y="520" width="20" height="20" />
		<rect x="520" y="520" width="20" height="20" />
		<rect x="560" y="520" width="20" height="20" />
		<rect x="580" y="520" width="20" height="20" />
		<rect x="600" y="520" width="20" height="20" />
		<rect x="640" y="520" width="20" height="20" />
		<rect x="300" y="540" width="20" height="20" />
		<rect x="360" y="540" width="20" height="20" />
		<rect x="420" y="540" width="20" height="20" />
		<rect x="440" y="540" width="20" height="20" />
		<rect x="480" y="540" width="20" height="20" />
		<rect x="560" y="540" width="20" height="20" />
		<rect x="600" y="540" width="20" height="20" />
		<rect x="620" y="540" width="20" height="20" />
		<rect x="240" y="560" width="20" height="20" />
		<rect x="280" y="560" width="20" height="20" />
		<rect x="300" y="560" width="20" height="20" />
		<rect x="320" y="560" width="20" height="20" />
		<rect x="340" y="560" width="20" height="20" />
		<rect x="360" y="560" width="20" height="20" />
		<rect x="400" y="560" width="20" height="20" />
		<rect x="420" y="560" width="20" height="20" />
		<rect x="440" y="560" width="20" height="20" />
		<rect x="460" y="560" width="20" height="20" />
		<rect x="480" y="560" width="20" height="20" />
		<rect x="500" y="560" width="20" height="20" />
		<rect x="520" y="560" width="20" height="20" />
		<rect x="540" y="560" width="20" height="20" />
		<rect x="560" y="560" width="20" height="20" />
		<rect x="580" y="560" width="20" height="20" />
		<rect x="640" y="560" width="20" height="20" />
		<rect x="280" y="580" width="20" height="20" />
		<rect x="300" y="580" width="20" height="20" />
		<rect x="340" y="580" width="20" height="20" />
		<rect x="400" y="580" width="20" height="20" />
		<rect x="440" y="580" width="20" height="20" />
		<rect x="540" y="580" width="20" height="20" />
		<rect x="580" y="580" width="20" height="20" />
		<rect x="600" y="580" width="20" height="20" />
		<rect x="620" y="580" width="20" height="20" />
		<rect x="280" y="600" width="20" height="20" />
		<rect x="300" y="600" width="20" height="20" />
		<rect x="320" y="600" width="20" height="20" />
		<rect x="380" y="600" width="20" height="20" />
		<rect x="400" y="600" width="20" height="20" />
		<rect x="440" y="600" width="20" height="20" />
		<rect x="460" y="600" width="20" height="20" />
		<rect x="520" y="600" width="20" height="20" />
		<rect x="560" y="600" width="20" height="20" />
		<rect x="600" y="600" width="20" height="20" />
		<rect x="620" y="600" width="20" height="20" />
		<rect x="640" y="600" width="20" height="20" />
		<rect x="260" y="620" width="20" height="20" />
		<rect x="420" y="620" width="20" height="20" />
		<rect x="440" y="620" width="20" height="20" />
		<rect x="460" y="620" width="20" height="20" />
		<rect x="520" y="620" width="20" height="20" />
		<rect x="540" y="620" width="20" height="20" />
		<rect x="560" y="620" width="20" height="20" />
		<rect x="580" y="620" width="20" height="20" />
		<rect x="600" y="620" width="20" height="20" />
		<rect x="240" y="640" width="20" height="20" />
		<rect x="340" y="640" width="20" height="20" />
		<rect x="360" y="640" width="20" height="20" />
		<rect x="420" y="640" width="20" height="20" />
		<rect x="440" y="640" width="20" height="20" />
		<rect x="460" y="640" width="20" height="20" />
		<rect x="520" y="640" width="20" height="20" />
		<rect x="560" y="640" width="20" height="20" />
		<rect x="620" y="640" width="20" height="20" />
		<path d="M80,80 h140 v140 h-140 Z M100.0,100.0 h100.0 v100.0 h-100.0 Z" fill-rule="evenodd" />
		<path d="M520,80 h140 v140 h-140 Z M540.0,100.0 h100.0 v100.0 h-100.0 Z" fill-rule="evenodd" />
		<rect x="120" y="120" width="60" height="60" />
		<rect x="560" y="120" width="60" height="60" />
		<path d="M80,520 h140 v140 h-140 Z M100.0,540.0 h100.0 v100.0 h-100.0 Z" fill-rule="evenodd" />
		<rect x="120" y="560" width="60" height="60" />
	</svg>
</div>
