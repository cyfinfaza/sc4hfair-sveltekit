"""

Updates schema for validating tent slugs

python tentsToContentfulSchema.py

"""

import contentful
import json

tentSlugs = json.load(open('../src/data/tentSlugs.json'))
listOfTents = list(tentSlugs.keys())
listOfTents.insert(0, '') # so we can say none

def updateContentType(id):
	print('updating', id)
	ct = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{id}').json()

	for field in ct['fields']:
		if field['id'] == 'tent':
			flag = False
			for valid in field['validations']:
				if 'in' in valid:
					valid['in'] = listOfTents
					flag = True
			if not flag:
				field['validations'].append({
					'in': listOfTents
				})
			break

	version = str(ct['sys']['version'])
	del ct['sys']

	req = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{id}', json=ct, headers={
		'X-Contentful-Version': version,
	})
	# print(req.status_code, req.text)

	version = str(req.json()['sys']['version'])

	# activate version
	req = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{id}/published', headers={
		'X-Contentful-Version': version,
	})
	# print(req.status_code, req.text)

updateContentType('scheduledEvent')
updateContentType('club')