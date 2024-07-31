"""

Patches Contentful club entries with the tent they belong to
Makes it easier to do this at a later date

python tentsToContentful.py

possible arguments:
	--no-publish - don't publish the entries after updating them

"""

import contentful
import json

contentTypeId = 'club'

tentData: dict[str, list[str]] = json.load(open('tentsToClubs.json'))

# get list of all previous entries
# the update api requires the version number of the entry to be updated
# we can grab them all in bulk at the start
entries = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version,fields.slug&sys.archivedAt[exists]=false').json()

if entries['total'] > entries['limit']:
	print('todo: implement paging')

previousData = {}
for entry in entries['items']:
	previousData[entry['fields']['slug']['en-US']] = (entry['sys']['id'], entry['sys']['version'])

publishPayload = []

for tentKey in tentData:
	for clubSlug in tentData[tentKey]:
		if clubSlug not in previousData:
			print('skipping, unknown', clubSlug)
			continue

		entryId, version = previousData[clubSlug]
		print('updating', clubSlug)

		req = contentful.session.patch(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{entryId}', headers={
			'Content-Type': 'application/json-patch+json',
			'X-Contentful-Version': str(version),
		}, json=[{"op": "add", "path": "/fields/tent", "value": {"en-US": tentKey}}])

		if req.status_code != 200:
			print('failed', req.status_code, req.text)
			continue

		publishPayload.append({
			'sys': {
				'id': entryId,
				'type': 'Link',
				'linkType': 'Entry',
				'version': req.json()['sys']['version'],
			}
		})

contentful.conditionalBulkPublish(publishPayload)