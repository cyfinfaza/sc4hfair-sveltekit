from datetime import datetime
from dateutil.tz import UTC
from flask import Blueprint, request, session, Response
from uuid import uuid4
import json

from util import mongo

bp = Blueprint('pvt', __name__, url_prefix='/pvt')

db = mongo.analytics
sessionsCollection = db.sessions
requestsCollection = db.requests

@bp.before_request
def make_session_permanent():
	session.permanent = True

@bp.route('/', methods=['POST'])
def track():
	if 'track_id' not in session:
		session['track_id'] = str(uuid4())
		return 'unconfirmed'

	report = request.get_json(force=True)
	if not report:
		return Response('invalid', 400)

	agent = str(request.user_agent)

	if len(json.dumps(report)) > 300 or len(agent) > 200:
		return Response('length limit exceeded', 413)

	if 'url' not in report:
		return Response('missing url', 400)

	url = report['url']
	requestDocument = {'track_id': session['track_id'], 'url': url, 't': datetime.now(tz=UTC)}
	if 'meta' in report:
		requestDocument['meta'] = report['meta']

	sessionsCollection.update_one(
		{'_id': session['track_id']}, {'$set': {'agent': agent}}, upsert=True
	)
	requestsCollection.insert_one(requestDocument)

	return Response('ok', 201)

@bp.route('/', methods=['GET'])
def status():
		if 'track_id' not in session:
			return Response('invalid pvt_s', 404)

		sess = sessionsCollection.find_one({'_id': session['track_id']})
		reqsC = requestsCollection.count_documents({'track_id': session['track_id']})
		if sess:
			return Response(f"{sess['agent']}<br>{reqsC}", 200)

		return Response('no data', 404)