declare namespace App {
	interface Error {
		name?: string;
		message?: string;
		stack?: string;
	}
	// interface Locals {}
	// interface PageData {}
	// interface Platform {}
}

declare namespace svelteHTML {
	interface HTMLAttributes {
		'on:error'?: (event: ErrorEvent) => void;
		'onclick'?: string; // make extra sure to run if js fails to load
	}
}
