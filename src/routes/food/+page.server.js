import { queryContentful } from 'logic/contentful.js';

const query = `{
	foodVendorCollection(order: name_ASC) {
		items {
			name
			items
		}
	}
}`;

/**
 * @typedef {object} FoodVendor
 * @property {string} name
 * @property {{ key: string; value: string; id: string }[]} items
 */

let loadedData = false,
	/** @type {FoodVendor[]} */
	foodVendors = [];

/** @type {import('./$types').PageServerLoad} */
export async function load() {
	if (!loadedData) {
		/** @type {{ foodVendorCollection: { items: FoodVendor[] } }} */
		const resp = await queryContentful(query);

		foodVendors = resp.foodVendorCollection?.items;

		loadedData = true;
	}

	return { foodVendors };
}
