import tentSlugs from 'data/tentSlugs.json';
import { queryContentful } from 'logic/contentful.js';

// big limit to make sure we get all events!!, default is 100 but we have 200+ events
const query = `{
	scheduledEventCollection(order: time_ASC, limit: 500) {
		items {
			sys {
				id
			}
			title
			time
			endTime
			tent
			near
		}
	}
}`;

/**
 * @typedef {object} Event
 * @property {object} sys
 * @property {string} sys.id
 * @property {string} title
 * @property {string} time
 * @property {string | null} endTime
 * @property {keyof typeof tentSlugs | null} tent
 * @property {boolean | null} near
 */

/** @type {(Event & { tentName: string | null })[]} */
let events = [],
	/** @type {('All' | keyof typeof tentSlugs)[]} */
	eventTentsList = [];

/** @satisfies {import('./$types').PageServerLoad} */
export async function load() {
	if (events.length === 0) {
		/** @type {{ scheduledEventCollection: { items: Event[] } }} */
		const resp = await queryContentful(query);
		events = resp.scheduledEventCollection?.items.map((element) => {
			return {
				...element,
				tentName: (element.tent && tentSlugs[element.tent]) || element.tent, // for search
			};
		});

		eventTentsList = [
			/** @type {const} */ ('All'),
			...new Set(events.map((event) => event.tent)),
		].filter(
			/**
			 * @template T
			 * @param {T | null} tent
			 * @returns {tent is T}
			 */
			(tent) => tent !== null
		);
	}

	return { events, eventTentsList };
}
