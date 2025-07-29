from datetime import datetime
from flask import Blueprint, g

from ._util import auth_required, mongo, success_json, error_json

bp = Blueprint('interests', __name__, url_prefix='/interests')

db = mongo.users
interests = db.interests

@bp.before_request
@auth_required
def before_request():
	g.current_year = datetime.now().year
	pass

@bp.route('/', methods=['GET'])
def get_interests():
	res = interests.aggregate([
		{'$match': {'user_id': g.user_id, 'year': g.current_year}},
		{'$group': {'_id': None, 'interests': {'$addToSet': '$slug'}}},
		{'$project': {'_id': False, 'interests': True}}
	])

	interests_list = next(res, {
		'interests': []
	})

	return success_json(data=interests_list)

@bp.route('/', methods=['DELETE'])
def delete_all_interests():
	result = interests.delete_many({'user_id': g.user_id, 'year': g.current_year})

	return success_json(result.deleted_count)

@bp.route('/<slug>', methods=['PUT'])
def add_interest(slug):
	doc = {
		'user_id': g.user_id,
		'slug': slug,
		'year': g.current_year
	}
	result = interests.update_one(doc, {'$setOnInsert': doc}, upsert=True)

	return success_json(status=201 if result.upserted_id is not None else 200)

@bp.route('/<slug>', methods=['DELETE'])
def delete_interest(slug):
	result = interests.delete_one({'user_id': g.user_id, 'slug': slug, 'year': g.current_year})

	if result.deleted_count == 0:
		return error_json(status=404)

	return success_json()