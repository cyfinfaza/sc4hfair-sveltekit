from flask import g, request, Response
from bson import json_util, ObjectId
import jwt
from os import environ
from pymongo import MongoClient

mongo = MongoClient(environ.get('MONGODB_SECRET'))

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

JWT_SECRET = environ.get('JWT_SECRET')

def auth_required(f):
	def wrapper(*args, **kwargs):
		session_token = request.cookies.get('session_token')

		if not session_token:
			return error_json('Not authenticated', status=401)

		try:
			payload = jwt.decode(session_token, JWT_SECRET, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			return error_json('Session expired', status=401)
		except jwt.InvalidTokenError:
			return error_json('Invalid session token', status=401)
		except Exception as e:
			return error_json(f'Error decoding session token: {str(e)}', status=401)

		g.user_id = ObjectId(payload['sub'])

		return f(*args, **kwargs)

	wrapper.__name__ = f.__name__
	return wrapper