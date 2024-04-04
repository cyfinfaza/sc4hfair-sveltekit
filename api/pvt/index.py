from datetime import datetime, timedelta
from flask import Flask, request, session, Response
from flask_cors import CORS
import pymongo
from uuid import uuid4
import dotenv
from os import environ
import json

dotenv.load_dotenv()
MONGODB_SECRET = environ.get('PVT_MONGODB')

client = pymongo.MongoClient(MONGODB_SECRET)
db = client.analytics
sessionsCollection = db.sessions
requestsCollection = db.requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.update(SESSION_COOKIE_NAME='pvt_s', SESSION_COOKIE_SAMESITE='None', SESSION_COOKIE_SECURE=True, PERMANENT_SESSION_LIFETIME=timedelta(days=365))
# DO NOT CHANGE THIS UNLESS YOU WANT ALL REGISTERED SESSIONS TO BREAK
app.secret_key = '--------'

@app.before_request
def make_session_permanent():
	session.permanent = True

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
	if request.method == 'POST':
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
		requestDocument = {'track_id': session['track_id'], 'url': url, 't': datetime.utcnow()}
		if 'meta' in report:
			requestDocument['meta'] = report['meta']

		sessionsCollection.update_one(
			{'_id': session['track_id']}, {'$set': {'agent': agent}}, upsert=True
		)
		requestsCollection.insert_one(requestDocument)

		return Response('ok', 201)

	elif request.method == 'GET':
		if 'track_id' not in session:
			return Response('invalid pvt_s', 404)

		sess = sessionsCollection.find_one({'_id': session['track_id']})
		reqsC = requestsCollection.count_documents({'track_id': session['track_id']})
		if sess:
			return Response(f"{sess['agent']}<br>{reqsC}", 200)

		return Response('no data', 404)

if __name__ == '__main__':
	app.run(debug=True, port=5006)
