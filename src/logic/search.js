export function exactSearch(objList, priorityKey, secondaryKeys, query) {
	function prepare(text) {
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
		return objList
			.filter((obj) => getObjValue(obj, priorityKey).indexOf(query) !== -1)
			.concat(
				objList.filter(
					(obj) =>
						secondaryKeys.some((key) => getObjValue(obj, key).indexOf(query) !== -1) &&
						getObjValue(obj, priorityKey).indexOf(query) === -1
				)
			);
	} else {
		return objList;
	}
}
