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

export async function load() {
	const resp = await queryContentful(query);

	// cleanup the data during build instead of at runtime on every client

	let clubsByTent = {};
	resp.clubCollection?.items.forEach((club) => {
		if (!club.tent) return;
		let tent = club.tent;
		if (!clubsByTent[tent]) clubsByTent[tent] = [];
		delete club.tent;
		clubsByTent[tent].push(club);
	});

	let eventsByTent = {};
	resp.scheduledEventCollection?.items.forEach((event) => {
		if (!event.tent) return;
		let tent = event.tent;
		if (!eventsByTent[tent]) eventsByTent[tent] = [];
		delete event.tent;
		event.id = event.sys.id;
		delete event.sys;
		eventsByTent[tent].push(event);
	});

	return { eventsByTent, clubsByTent };
}
