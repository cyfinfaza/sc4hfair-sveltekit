# fmt: off
from datetime import datetime
import dateutil.parser
from dateutil.tz import UTC
from flask import Flask, request, session, Response
from flask_cors import CORS
import pymongo
import dotenv
from os import environ
from pywebpush import webpush, WebPushException
import json
from bson import json_util
from uuid import uuid4
from functools import wraps

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, origins=['*'], supports_credentials=True)
app.config.update(SESSION_COOKIE_NAME='pvt_s', SESSION_COOKIE_SAMESITE='None', SESSION_COOKIE_SECURE=True)
app.secret_key = '--------'

dotenv.load_dotenv()
MONGODB_SECRET = environ.get('MONGODB_SECRET')
WEBPUSH_PRIVATE_KEY = environ.get('WEBPUSH_PRIVATE_KEY')

client = pymongo.MongoClient(MONGODB_SECRET)
db = client.webpush
subscriptionsCollection = db.subscriptions
scheduledNotificationsCollection = db.scheduledNotifications

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

def json_response(status, message=None, data=None):
	d = {}
	if 100 <= status <= 399: d['type'] = 'success'
	elif 400 <= status <= 599: d['type'] = 'error'
	if data: d.update(data)
	if message: d['message'] = message
	return Response(json_util.dumps(d), status=status, mimetype='application/json')

def success_json(message=None, data=None, status=200):
	return json_response(status, message, data)
def error_json(message=None, data=None, status=400):
	return json_response(status, message, data)

# show number of subscriptions
@app.route('/api/webpush', methods=['GET'])
def index():
	res = subscriptionsCollection.aggregate([{
		'$group': {
			'_id': None,
			'subscriptions': {'$sum': {
				'$cond': [{'$ne': ['$valid', False]}, 1, 0]
			}},
			'invalidSubscriptions': {'$sum': {
				'$cond': [{'$eq': ['$valid', False]}, 1, 0]
			}},
		},
	}]).next()
	return success_json(data={
		'subscriptions': res['subscriptions'],
		'invalidSubscriptions': res['invalidSubscriptions'],
	})

# add (or check if dry) subscription
@app.route('/api/webpush/subscribe', methods=['POST'], endpoint='subscribe')
# remove subscription
@app.route('/api/webpush/unsubscribe', methods=['POST'], endpoint='unsubscribe')
# pushsubscriptionchange event
@app.route('/api/webpush/resubscribe', methods=['POST'], endpoint='resubscribe')
def main():
	'''main route with common logic'''

	data = request.get_json() or {}

	sub_info = data.get('subscription')
	if request.endpoint != 'resubscribe':
		if sub_info is None: return error_json('No subscription info')

	print('sub_info', sub_info)
	print('pvt id', 'track_id' in session and session['track_id'])

	alreadyExists = subscriptionsCollection.count_documents({'subscription_info': sub_info, 'valid': {'$ne': False}}) > 0

	if request.endpoint == 'subscribe':
		test_id = str(uuid4())

		dry = 'dry' in request.args

		# check sub by sending test notif if necessary
		# if we're dry, we can just reply if the sub exists
		if (not dry) and (not test_webpush(sub_info, test_id)):
			return error_json(message='Test failed')

		# modify db if necessary
		if not dry:
			subscriptionsCollection.update_one({'subscription_info': sub_info}, {'$set': {
				'created': datetime.now(tz=UTC),
				'subscription_info': sub_info,
				'user_agent': str(request.user_agent),
				'track_id': 'track_id' in session and session['track_id'] or None,
				'valid': None # we just got it, it should be fine
			}}, upsert=True)

		return success_json(data={
			'already_exists': alreadyExists,
			'registered': alreadyExists if dry else True, # if the subscription is in the db
			'test_id': None if dry else test_id
		})

	elif request.endpoint == 'unsubscribe':
		if not alreadyExists:
			return error_json(data={
				'already_exists': False,
			}, message='Subscription does not exist')

		subscriptionsCollection.delete_one({'subscription_info': sub_info})

		return success_json(data={
			'registered': False,
		})

	elif request.endpoint == 'resubscribe':
		result = 'noChange'

		oldSubscription = data.get('oldSubscription')
		print('oldSubscription', oldSubscription)

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
			op = subscriptionsCollection.update_one(query, {'$set': {
				'created': datetime.now(tz=UTC),
				'subscription_info': sub_info,
				'user_agent': str(request.user_agent),
				'track_id': 'track_id' in session and session['track_id'] or None,
				'valid': None
			}}, upsert=True)
			if op.upserted_id is None:
				result = 'oldUpdated'
			else:
				result = 'newCreated'

		# if we only have an old subscription, just delete the entry
		elif oldSubscription and 'endpoint' in oldSubscription:
			op = subscriptionsCollection.delete_one(query)
			if op.deleted_count > 0:
				result = 'oldDeleted'

		return success_json(data={
			'result': result,
			'already_exists': alreadyExists,
		})

def check_subscription_info():
	'''
	Retrieves subscription info from query for GET or json body for anything else and passes it on
	'''
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			sub_info = None

			if request.method == 'GET':
				if 'subscription' in request.args:
					try:
						sub_info = json.loads(request.args.get('subscription'))
					except json.decoder.JSONDecodeError:
						return error_json('Invalid subscription')
			else:
				sub_info = (request.get_json() or {}).get('subscription')

			if sub_info is None: return error_json('No subscription info')
			request.environ['sub_info'] = sub_info

			return f(*args, **kwargs)
		return wrapper
	return decorator

@app.route('/api/webpush/scheduledNotifications', methods=['GET'])
@check_subscription_info()
def get_all_scheduled_notifications():
	pipeline = [
		# match the subscription by sub_info
		{
			'$match': {
				'subscription_info': {
					'$eq': request.environ['sub_info']
				}
			}
		},
		# lookup scheduled notifications
		{
			'$lookup': {
				'from': 'scheduledNotifications',
				'localField': '_id',
				'foreignField': 'target',
				'as': 'notifications'
			}
		},
		# project to reshape the output
		{
			'$project': {
				'_id': False,
				'subscriptionId': {'$toString': '$_id'},
				'eventIds': {
					'$map': {
						'input': '$notifications',
						'as': 'notification',
						'in': '$$notification.eventId'
					}
				}
			}
		}
	]

	result = list(subscriptionsCollection.aggregate(pipeline))

	if len(result) == 0:
		return error_json('Subscription not found')

	return success_json(data=result[0])

@app.route('/api/webpush/scheduledNotifications', methods=['POST'])
@check_subscription_info()
def create_scheduled_notification():
	data = request.get_json() or {}

	when = dateutil.parser.isoparse(data.get('when'))
	now = datetime.now(tz=UTC)

	if when < now: return error_json('Notification time must be in the future')

	sub_info = request.environ['sub_info']
	subscription = subscriptionsCollection.find_one({'subscription_info': sub_info}, projection={'_id': True})
	if not subscription: return error_json('Subscription not found')

	notification = {
		'target': subscription['_id'],
		'eventId': data.get('eventId'),
		'when': when,
		'created': now,
	}

	result = scheduledNotificationsCollection.find_one_and_update(
		{'target': subscription['_id'], 'eventId': data.get('eventId')},
		{'$set': notification}, # update the record, allows us to change the time if we want
		upsert=True,
		return_document=pymongo.ReturnDocument.AFTER
	)

	return success_json(data={'notification': result})

@app.route('/api/webpush/scheduledNotifications', methods=['DELETE'])
@check_subscription_info()
def delete_scheduled_notification():
	data = request.get_json() or {}

	sub_info = request.environ['sub_info']
	subscription = subscriptionsCollection.find_one({'subscription_info': sub_info}, projection={'_id': True})
	if not subscription: return error_json('Subscription not found')

	delete_result = scheduledNotificationsCollection.delete_one({
		'target': subscription['_id'],
		'eventId': data.get('eventId')
	})

	if delete_result.deleted_count == 0:
		return error_json('Notification not found or already deleted')

	return success_json()

if __name__ == '__main__':
	app.run(debug=True, port=6002)
