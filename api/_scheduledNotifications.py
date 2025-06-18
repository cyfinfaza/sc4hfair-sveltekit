from datetime import datetime
import dateutil.parser
from dateutil.tz import UTC
from flask import Blueprint, g, request
from functools import wraps
import json
from pymongo import ReturnDocument

from ._util import mongo, success_json, error_json

bp = Blueprint('scheduledNotifications', __name__, url_prefix='/webpush/scheduledNotifications')

db = mongo.webpush
scheduledNotificationsCollection = db.scheduledNotifications
subscriptionsCollection = db.subscriptions

def sub_info_required(f):
	'''
	Retrieves subscription info from query for GET or json body for anything else and passes it on
	'''
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
		g.sub_info = sub_info

		return f(*args, **kwargs)

	wrapper.__name__ = f.__name__
	return wrapper

@bp.route('/', methods=['GET'])
@sub_info_required
def get_all_scheduled_notifications():
	pipeline = [
		# match the subscription by sub_info
		{
			'$match': {
				'subscription_info': {
					'$eq': g.sub_info
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

@bp.route('/', methods=['POST'])
@sub_info_required
def create_scheduled_notification():
	data = request.get_json() or {}

	when = dateutil.parser.isoparse(data.get('when'))
	now = datetime.now(tz=UTC)

	if when < now: return error_json('Notification time must be in the future')

	subscription = subscriptionsCollection.find_one({'subscription_info': g.sub_info}, projection={'_id': True})
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
		return_document=ReturnDocument.AFTER
	)

	return success_json(data={'notification': result})

@bp.route('/', methods=['DELETE'])
@sub_info_required
def delete_scheduled_notification():
	data = request.get_json() or {}

	subscription = subscriptionsCollection.find_one({'subscription_info': g.sub_info}, projection={'_id': True})
	if not subscription: return error_json('Subscription not found')

	delete_result = scheduledNotificationsCollection.delete_one({
		'target': subscription['_id'],
		'eventId': data.get('eventId')
	})

	if delete_result.deleted_count == 0:
		return error_json('Notification not found or already deleted')

	return success_json()