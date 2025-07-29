from flask import Blueprint, g, request
from pymongo import ReturnDocument

from ._util import auth_required, mongo, success_json, error_json

bp = Blueprint('profile', __name__, url_prefix='/profile')

db = mongo.users
users = db.users

editable_fields = ['name', 'preferred_email', 'phone', 'graduation']
profile_projection = { '_id': False, 'email': True } | { field: True for field in editable_fields }

@bp.route('/', methods=['GET'])
@auth_required
def get_profile():
	user = users.find_one({'_id': g.user_id}, projection=profile_projection)

	if not user:
		return error_json('User not found', status=404)

	return success_json(data={'profile': user})

@bp.route('/', methods=['PATCH'])
@auth_required
def update_profile():
	data = request.get_json() or {}

	# Validate and sanitize input data as needed
	updates = {}
	for field in editable_fields:
		if field in data:
			value = data[field]
			if value is None or (isinstance(value, str) and not value.strip()):
				continue
			if (field == 'graduation') and (not isinstance(value, str) or not value.isdigit()) or field == 'email' and (not isinstance(value, str) or '@' not in value):
				return error_json(f'Invalid {field}')
			updates[field] = value

	if not updates:
		return error_json('No valid fields to update')

	user = users.find_one_and_update(
		{'_id': g.user_id},
		{'$set': updates},
		projection=profile_projection,
		upsert=False,
		return_document=ReturnDocument.AFTER
	)

	if not user:
		return error_json('User not found', status=404)

	return success_json(data={'profile': user})