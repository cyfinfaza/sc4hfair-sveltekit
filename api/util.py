from flask import Response
from bson import json_util
from os import environ
import pymongo

mongo = pymongo.MongoClient(environ.get('MONGODB_SECRET'))

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