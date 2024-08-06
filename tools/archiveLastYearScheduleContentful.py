import contentful
import requests

contentTypeId = 'scheduledEvent'

(webhookPreviousActive, webhookUrl) = contentful.setWebhookActive(contentful.vercelWebhookId, False)
print('webhook disabled')

# get list of all previous entries
# the update api requires the version number of the entry to be updated
entries = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version&sys.archivedAt[exists]=false&metadata.tags.sys.id[in]={contentful.lastYearTagId}&limit=1000').json()
if entries['total'] > entries['limit']: print('todo: implement paging')

unPublishPayload = []

for entry in entries['items']:
	id = entry['sys']['id']

	unPublishPayload.append({
		'sys': {
			'id': id,
			'type': 'Link',
			'linkType': 'Entry'
		}
	})

contentful.bulkAction(unPublishPayload, 'unpublish')

for entry in entries['items']:
	id = entry['sys']['id']
	version = entry['sys']['version']

	res = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/archived', headers={
		'X-Contentful-Content-Type': contentTypeId,
		'X-Contentful-Version': str(version)
	})
	print('archived', id, res.status_code)

if webhookPreviousActive:
	contentful.setWebhookActive(contentful.vercelWebhookId, True) # reenable
	requests.get(webhookUrl) # manually trigger