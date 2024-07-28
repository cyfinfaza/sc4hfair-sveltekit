/**
 * @param {string} query
 * @param {{[key: string]: string, items?: [{key: string, value: string}]}[]} objList
 * @param {string} priorityKey
 * @param {string[]} secondaryKeys
 * @param {boolean} searchItemsKV for use with contentful repeater type data, see food for example usage
 */
export function exactSearch(
	query,
	objList,
	priorityKey,
	secondaryKeys = [],
	searchItemsKV = false
) {
	function prepare(text) {
		if (Array.isArray(text)) text = text.join(',');
		if (typeof text !== 'string') {
			console.error('exactSearch error: cannot prepare non-string', text);
			text = '';
		}
		return text
			.trim()
			.toLowerCase()
			.normalize('NFKD')
			.replace(/[\u0300-\u036f]/g, '')
			.replace(/4(?:-|\u2010|\u2011)?h/g, '4h');
	}

	const getObjValue = (obj, key) => prepare(new Function('obj', `return obj.${key}`)(obj));

	query = prepare(query);
	// console.log('exactSearch query:', query);
	if (query) {
		// search for exact match, returning first objects that match primary key, then secondary key
		let results = objList;
		if (searchItemsKV) {
			results = results.map((obj) => ({
				...obj,
				items: obj.items.filter(
					(item) =>
						prepare(item.key).indexOf(query) !== -1 || prepare(item.value).indexOf(query) !== -1
				),
			}));
		} else {
			results = results.filter((obj) => getObjValue(obj, priorityKey).indexOf(query) !== -1);
		}
		if (secondaryKeys.length)
			results = results.concat(
				objList.filter(
					(obj) =>
						(!searchItemsKV ||
							results.some(
								(robj) => getObjValue(obj, priorityKey) == getObjValue(robj, priorityKey)
							)) && // don't duplicate
						secondaryKeys.some((key) => getObjValue(obj, key).indexOf(query) !== -1)
				)
			);
		return [...new Set(results)];
	} else {
		return objList;
	}
}
