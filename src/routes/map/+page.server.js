import { queryContentful } from 'logic/contentful.js';

const query = `{
	scheduledEventCollection(order: time_ASC, limit: 500, where: {time_gt: "${new Date().toISOString()}"}) {
		items {
			sys {
				id
			}
			title
			time
			endTime
			tent
		}
	}
	clubCollection(order: name_ASC) {
		items {
			name
			slug
			tent
		}
	}
}`;

let loadedData = false,
	/** @type {{ [tent: string]: { name: string; slug: string }[] }} */
	clubsByTent = {},
	/**
	 * @type {{
	 * 	[tent: string]: { id: string; title: string; time: string; endTime: string | null }[];
	 * }}
	 */
	eventsByTent = {};

export async function load() {
	if (!loadedData) {
		/**
		 * @type {{
		 * 	scheduledEventCollection: {
		 * 		items: {
		 * 			sys: { id: string };
		 * 			title: string;
		 * 			time: string;
		 * 			endTime: string | null;
		 * 			tent: string;
		 * 		}[];
		 * 	};
		 * 	clubCollection: { items: { name: string; slug: string; tent: string }[] };
		 * }}
		 */
		const resp = await queryContentful(query);

		// cleanup the data during build instead of at runtime on every client

		resp.scheduledEventCollection?.items.forEach((event) => {
			if (!event.tent) return;
			let { tent, sys, ...newEvent } = { ...event, id: event.sys.id };
			if (!eventsByTent[tent]) eventsByTent[tent] = [];
			eventsByTent[tent].push(newEvent);
		});

		resp.clubCollection?.items.forEach((club) => {
			if (!club.tent) return;
			let { tent, ...filteredClub } = club;
			if (!clubsByTent[tent]) clubsByTent[tent] = [];
			clubsByTent[tent].push(filteredClub);
		});

		loadedData = true;
	}

	return { eventsByTent, clubsByTent };
}
