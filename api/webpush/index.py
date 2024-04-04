# fmt: off
from datetime import datetime
from flask import Flask, request, session, Response
from flask_cors import CORS
import pymongo
import dotenv
from os import environ
from pywebpush import webpush, WebPushException
import json
from uuid import uuid4

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
	return Response(json.dumps(d), status=status, mimetype='application/json')

def success_json(message=None, data=None):
	return json_response(200, message, data)
def error_json(message=None, data=None):
	return json_response(400, message, data)

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
				'created': datetime.utcnow(),
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
				'created': datetime.utcnow(),
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

if __name__ == '__main__':
	app.run(debug=True, port=6002)
