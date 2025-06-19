import tentSlugs from 'data/tentSlugs.json';
import { queryContentful } from 'logic/contentful';

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

export interface Event {
	sys: {
		id: string;
	};
	title: string;
	time: string;
	endTime: string | null;
	tent: keyof typeof tentSlugs | null;
	near: boolean | null;
}

let events: (Event & { tentName: string | null })[] = [],
	eventTentsList: ('All' | keyof typeof tentSlugs)[] = [];

export const load: import('./$types').PageServerLoad = async () => {
	if (events.length === 0) {
		/** @type {{ scheduledEventCollection: { items: Event[] } }} */
		const resp: { scheduledEventCollection: { items: Event[] } } = await queryContentful(query);
		events = resp.scheduledEventCollection?.items.map((element) => {
			return {
				...element,
				tentName: (element.tent && tentSlugs[element.tent]) || element.tent, // for search
			};
		});

		eventTentsList = ['All' as const, ...new Set(events.map((event) => event.tent))].filter(
			<T>(tent: T | null): tent is T => tent !== null
		);
	}

	return { events, eventTentsList };
};
