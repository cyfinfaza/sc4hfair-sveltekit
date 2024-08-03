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

let events = [],
	/** @type {string[]} */
	eventTentsList = [];

/** @satisfies {import('./$types').PageServerLoad} */
export async function load() {
	if (events.length === 0) {
		const resp = await queryContentful(query);
		events = resp.scheduledEventCollection?.items.map((element) => {
			return {
				...element,
				tentName: tentSlugs[element.tent] || element.tent, // for search
			};
		});

		eventTentsList = ['All', ...new Set(events.map((event) => event.tent))].filter(Boolean);
	}

	return { events, eventTentsList };
}
