from datetime import datetime
from dateutil.tz import UTC
from flask import Blueprint, request, session
import json
from os import environ
from pymongo import ReturnDocument
from pywebpush import webpush, WebPushException
from uuid import uuid4

from util import mongo, success_json, error_json

bp = Blueprint('webpush', __name__, url_prefix='/webpush')

db = mongo.webpush
subscriptionsCollection = db.subscriptions

# show number of subscriptions
@bp.route('/', methods=['GET'])
def index():
	since = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
	res = subscriptionsCollection.aggregate([
		{
			'$group': {
				'_id': None,
				'subscriptions': {'$sum': {
					'$cond': [{'$and': [{'$ne': ['$valid', False]}, {'$ne': ['$registered', False]}]}, 1, 0]
				}},
				'invalidSubscriptions': {'$sum': {
					'$cond': [{'$and': [{'$eq': ['$valid', False]}, {'$ne': ['$registered', False]}, {'$gt': ['$created', since]}]}, 1, 0]
				}},
				'unsubscribed': {'$sum': {
					'$cond': [{'$and': [{'$eq': ['$registered', False]}, {'$gt': ['$created', since]}]}, 1, 0]
				}}
			},
		},
		{
			'$project': {
				'_id': False
			}
		}
	]).next()
	return success_json(data=res)

WEBPUSH_PRIVATE_KEY = environ.get('WEBPUSH_PRIVATE_KEY')
def test_webpush(sub_info, id):
	'''Send a visible test notification, client should confirm it includes the correct id'''
	if not sub_info: return False
	try:
		webpush(
			subscription_info=sub_info,
			data=json.dumps({ 'type': 'test', 'id': id }),
			vapid_private_key=WEBPUSH_PRIVATE_KEY,
			vapid_claims={'sub': 'mailto:vapid_claims@4hcomputers.club'},
			# fix for windows (https://learn.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/push-request-response-headers)
			headers={'X-WNS-Type': 'wns/raw', 'X-WNS-Cache-Policy': 'no-cache'}
		)
		return True
	except WebPushException as e:
		print('WebPushException', e.args)
		print(e.response.text)
		print(e.response.headers)
		return False
	except Exception as e:
		print(e.args)
		return False

subscriptionIdProjection = {'_id': False, 'subscriptionId': {'$toString': '$_id'}}

# add (or check if dry) subscription
@bp.route('/subscribe', methods=['POST'], endpoint='subscribe')
# remove subscription
@bp.route('/unsubscribe', methods=['POST'], endpoint='unsubscribe')
# pushsubscriptionchange event
@bp.route('/resubscribe', methods=['POST'], endpoint='resubscribe')
def main():
	'''main route with common logic'''

	data = request.get_json() or {}

	sub_info = data.get('subscription')
	if request.endpoint != 'resubscribe':
		if sub_info is None: return error_json('No subscription info')
	
	oldSubscription = data.get('oldSubscription')

	print('sub_info', sub_info)
	print('pvt id', 'track_id' in session and session['track_id'])

	existing = subscriptionsCollection.find_one(
		{'subscription_info': sub_info, 'valid': {'$ne': False}, 'subscribed': {'$ne': False}},
		projection=subscriptionIdProjection
	)
	alreadyExists = existing is not None
	subscriptionId = existing['subscriptionId'] if existing else None

	if request.endpoint == 'subscribe':
		test_id = str(uuid4())

		dry = 'dry' in request.args

		# check sub by sending test notif if necessary
		# if we're dry, we can just reply if the sub exists
		if (not dry) and (not test_webpush(sub_info, test_id)):
			return error_json(message='Test failed')

		result = 'noChange'

		# modify db if necessary
		if not dry:
			update = {'$set': {
				'created': datetime.now(tz=UTC),
				'subscription_info': sub_info,
				'user_agent': str(request.user_agent),
				'track_id': 'track_id' in session and session['track_id'] or None,
				'valid': None, # we just got it, it should be fine
				'registered': True # just subscribed
			}}

			oldExisting = subscriptionsCollection.find_one(
				{'subscription_info': {'$exists': True, '$ne': None, '$eq': oldSubscription}},
				projection={'_id': True, 'subscriptionId': {'$toString': '$_id'}}
			) if oldSubscription is not None else None

			# overwrite old subscription with new (will update if old is same as new)
			if oldExisting:
				sub = subscriptionsCollection.find_one_and_update(
					{'_id': oldExisting['_id']},
					update,
					projection=subscriptionIdProjection,
					upsert=False,
					return_document=ReturnDocument.AFTER
				)
				subscriptionId = sub['subscriptionId']
				result = 'oldExistingUpdated'

			# create new subscription
			else:
				sub = subscriptionsCollection.find_one_and_update(
					{'subscription_info': sub_info},
					update,
					projection=subscriptionIdProjection,
					upsert=True,
					return_document=ReturnDocument.AFTER
				)
				subscriptionId = sub['subscriptionId']
				result = 'oldUpdated' if alreadyExists else 'newCreated'

		return success_json(data={
			'alreadyExists': alreadyExists,
			'registered': alreadyExists if dry else True, # if the subscription is in the db
			'testId': None if dry else test_id,
			'subscriptionId': subscriptionId,
			'result': result
		})

	elif request.endpoint == 'unsubscribe':
		if not alreadyExists:
			return error_json(data={
				'alreadyExists': False,
			}, message='Subscription does not exist')

		sub = subscriptionsCollection.update_one(
			{'subscription_info': sub_info},
			{'$set': {
				'registered': False,
			}},
			upsert=False
		)

		return success_json(data={
			'registered': False,
			'subscriptionId': subscriptionId
		})

	elif request.endpoint == 'resubscribe':
		result = 'noChange'

		if oldSubscription is None:
			return error_json('No old subscription info')

		subscriptionId = None

		query = {'subscription_info': {
			'$exists': True,
			'$ne': None,
			'$eq': oldSubscription
		}}
		if oldSubscription and 'endpoint' in oldSubscription:
			query = {'subscription_info': {
				'endpoint': oldSubscription['endpoint']
			}}

		# try updating the old entry if we can, otherwise create a new entry
		if sub_info and not alreadyExists: # newSubscription
			sub = subscriptionsCollection.find_one_and_update(
				query,
				{'$set': {
					'created': datetime.now(tz=UTC),
					'subscription_info': sub_info,
					'user_agent': str(request.user_agent),
					'track_id': 'track_id' in session and session['track_id'] or None,
					'valid': None
				}},
				projection={'_id': False, 'subscriptionId': {'$toString': '$_id'}},
				upsert=True,
				return_document=ReturnDocument.AFTER
			)
			if sub.upserted_id is None:
				result = 'oldUpdated'
			else:
				result = 'newCreated'
			subscriptionId = sub['subscriptionId']

		# if we only have an old subscription
		elif oldSubscription and 'endpoint' in oldSubscription:
			op = subscriptionsCollection.update_one(query, {'$set': {
				'valid': False,
			}})
			if op.modified_count > 0:
				result = 'oldUpdated'

		return success_json(data={
			'result': result,
			'alreadyExists': alreadyExists,
			'subscriptionId': sub['subscriptionId'] if not alreadyExists else None
		})