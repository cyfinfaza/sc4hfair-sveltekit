import { writable } from 'svelte/store';

/** @type {import('svelte/store').Writable<string[] | undefined>} */
export const subscribedEvents = writable(undefined);
