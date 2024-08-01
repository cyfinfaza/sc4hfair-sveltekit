import { queryContentful } from 'logic/contentful.js';

const query = `{
	foodVendorCollection(order: name_ASC) {
		items {
			name
			items
		}
	}
}`;

let loadedData = false,
	foodVendors = [];

export async function load() {
	if (!loadedData) {
		const resp = await queryContentful(query);

		foodVendors = resp.foodVendorCollection?.items;

		loadedData = true;
	}

	return { foodVendors };
}
