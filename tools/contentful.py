import dotenv
from os import environ
import requests
import sys
from time import sleep
from datetime import datetime
from uuid import uuid4

dotenv.load_dotenv()

spaceId = 'e34g9w63217k'
environmentId = 'master'
cmaToken = environ.get('CONTENTFUL_CMA_TOKEN')

# newYear.py will ensure tag has been created with name "year: XXXX" and id "XXXX" in the contentful web interface
currentYear = datetime.now().year
lastYearTagId = str(currentYear - 1)
yearTagId = str(currentYear)

session = requests.Session()
session.headers.update({
	'Authorization': 'Bearer ' + cmaToken,
	'Content-Type': 'application/vnd.contentful.management.v1+json',
})

noPublish = '--no-publish' in sys.argv

vercelWebhookId = '2pNxUMPQKUMQz2aIHSO65Y'

def setWebhookActive(webhookId, active) -> tuple[bool, str]:
	"""
	return: previous webhook active state, webhook url
	"""

	url = f'https://api.contentful.com/spaces/{spaceId}/webhook_definitions/{webhookId}'

	get = session.get(url)
	if get.status_code != 200:
		raise Exception(f'failed to get webhook {webhookId}: {get.json()}')

	data = get.json()

	previousActive = data['active']

	data['active'] = active

	version = data['sys']['version']
	del data['sys']

	put = session.put(url, json=data, headers={
		'X-Contentful-Version': str(version),
	})
	if put.status_code != 200:
		raise Exception(f'failed to put webhook {webhookId}: {put.json()}')
	
	return (previousActive, data['url'])

def bulkAction(bulkPayload, action):
	if len(bulkPayload) == 0: return

	bulkReq = session.post(f'https://api.contentful.com/spaces/{spaceId}/environments/{environmentId}/bulk_actions/{action}', json={
		'entities': {
			'items': bulkPayload,
		},
	})

	print(f'waiting on bulk {action}... status', bulkReq.status_code, bulkReq.json()['sys']['status'], bulkReq.json())

	# wait for bulk action to finish
	while True:
		sleep(5)
		statusReq = session.get(f'https://api.contentful.com/spaces/{spaceId}/environments/{environmentId}/bulk_actions/actions/{bulkReq.json()["sys"]["id"]}')
		status = statusReq.json()['sys']['status']
		print(f'waiting on bulk {action}... status', status)
		if status == 'succeeded':
			break
		elif status == 'failed':
			print(statusReq.json()['error'])
			break

def conditionalBulkPublish(bulkPayload, action='publish'):
	"""
	publish entries in bulk if there are any, including noPublish & webhook safety
	"""

	if noPublish or len(bulkPayload) == 0: return

	(webhookPreviousActive, webhookUrl) = setWebhookActive(vercelWebhookId, False)

	bulkAction(bulkPayload, action)

	if webhookPreviousActive:
		setWebhookActive(vercelWebhookId, True) # reenable
		requests.get(webhookUrl) # manually trigger

base62alphabet: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
base: int = len(base62alphabet)	
def to_base62(input: int):
	output = ''
	while input != 0:
		output = base62alphabet[input % base] + output
		input //= base
	return output

def new_id():
	return to_base62(uuid4().int)