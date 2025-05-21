import contentful

# existingTags = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/tags').json()

currentYear = contentful.yearTagId

print('current year', currentYear)

create = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/tags/{currentYear}', json={
	'name': f'year: {currentYear}',
	'sys': {
		'visibility': 'private',
		'id': currentYear,
		'type': 'Tag'
	}
})

if create.status_code == 409:
	print('year tag already exists', create.json())
else:
	print('created year tag', create.status_code, create.json())