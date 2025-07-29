from datetime import datetime, timedelta
from dateutil.tz import UTC
from flask import current_app, Blueprint, make_response, redirect, request
import jwt
from os import environ
from pymongo import ReturnDocument
import re
import requests
from urllib.parse import ParseResult, urlencode, urlparse, urlunparse

from ._util import mongo, success_json, error_json, JWT_SECRET

bp = Blueprint('auth', __name__, url_prefix='/auth')

db = mongo.users
users = db.users

# these are whitelisted in google oauth2
primary_hosts = (
	'sc4hfair.app',
	'localhost:5173'
)
all_hosts = primary_hosts + (
	r'(?:[\w-]+\.)?sc4hfair\.app',
	r'sc4hfair-sveltekit-[\w-]+-cys-projects-c57b2204\.vercel\.app',
	# todo: admin panel
	r'localhost:\d+',
)
def validate_host(host: str):
	for valid_host in all_hosts:
		if re.fullmatch(valid_host, host):
			return True
	return False

def get_google_callback(parsed_url: ParseResult):
	# this allows us to share the same callback URL across different hosts
	# a final redirect will send us back to the original host
	host = 'https://sc4hfair.app'
	if parsed_url.netloc in primary_hosts:
		host = parsed_url.scheme + '://' + parsed_url.netloc
	return f'{host}/api/auth/google-callback'

"""
Google OAuth2 authentication flow
1. User initiates authentication by visiting `/google-init?redirect=/some/path`.
2. The server redirects the user to Google's OAuth2 authorization endpoint.
3. User grants permission and Google redirects back to `/google-callback` with a code.
4. The server exchanges the code for tokens and retrieves user information.
5. The server creates or updates the user in the database and generates a session token.
6. The server redirects the user to the final redirect URL with the session token set in a cookie.
"""

@bp.route('/google-init', methods=['GET'])
def google_auth_init():
	base_url = 'https://accounts.google.com/o/oauth2/v2/auth'

	final_redirect = request.args.get('redirect')

	parsed_url = urlparse(final_redirect)
	if not validate_host(parsed_url.netloc):
		return error_json('Not allowed to redirect back to this host', status=401)

	google_callback = get_google_callback(parsed_url)
	
	current_app.logger.info({
		'request_host': request.host,
		'netloc': parsed_url.netloc,
		'google_callback': google_callback,
		'final_redirect': final_redirect,
	})
	
	params = {
		'client_id': environ.get('GOOGLE_CLIENT_ID'),
		'redirect_uri': google_callback,
		'state': final_redirect,
		'prompt': 'consent',
		'response_type': 'code',
		'include_granted_scopes': 'true',
		'scope': 'openid email profile',
		'access_type': 'offline'
	}
	
	# Construct the full authorization URL with encoded parameters.
	authorization_url = f"{base_url}?{urlencode(params)}"
	
	# Redirect the user to the Google authentication page.
	return redirect(authorization_url, code=302)

# this will always be run on a primary host
@bp.route('/google-callback', methods=['GET'])
def google_auth_callback():
	code = request.args.get('code')

	if not code:
		return error_json('Missing code parameter')

	final_redirect = request.args.get('state')
	parsed_url = urlparse(final_redirect)

	if not final_redirect or not validate_host(parsed_url.netloc):
		return error_json('Not allowed to redirect back to this host', status=401)

	tokens = requests.post('https://oauth2.googleapis.com/token', data={
		'client_id': environ.get('GOOGLE_CLIENT_ID'),
		'client_secret': environ.get('GOOGLE_CLIENT_SECRET'),
		'code': code,
		'grant_type': 'authorization_code',
		'redirect_uri': get_google_callback(parsed_url)
	}).json()

	if 'id_token' not in tokens:
		return error_json('missing token')

	# trusted from google
	idt = jwt.decode(tokens['id_token'], options={'verify_signature': False})

	provider_id = idt.get('sub', None)
	email = idt.get('email', None)

	user = users.find_one_and_update(
		{
			'provider': 'google',
			'provider_id': provider_id
		},
		{
			'$set': {
				'email': email, # could theoretically change
				'last_login': datetime.now(UTC),
				# 'roles': ['dev'],
			},
			'$setOnInsert': {
				'provider': 'google',
				'provider_id': provider_id, # stable
				'name': idt.get('name', None), # user changeable
				'preferred_email': email,
			},
		},
		upsert=True,
		return_document=ReturnDocument.AFTER
	)

	exp = datetime.now(tz=UTC) + timedelta(days=30)

	# this can be verified when used in secure apis
	session_token = jwt.encode({
		'sub': str(user['_id']),
		'email': email, # used for display
		'roles': user.get('roles', []),
		'exp': exp
	}, JWT_SECRET, algorithm='HS256') # todo: use RS256

	query = {
		'redirect': final_redirect,
		'token': session_token,
	}

	res = redirect(urlunparse((parsed_url.scheme, parsed_url.netloc, '/api/auth/set-session', '', urlencode(query), '')), code=302)
	return res

# sets a cookie then redirects to the final url
@bp.route('/set-session', methods=['GET'])
def set_session():
	final_redirect = request.args.get('redirect')
	session_token = request.args.get('token')

	if not session_token or not final_redirect or not validate_host(urlparse(final_redirect).netloc):
		return error_json('Invalid parameters')

	exp = jwt.decode(session_token, options={'verify_signature': False}).get('exp', None)

	res = redirect(final_redirect, code=302)
	res.set_cookie('session_token', session_token, path='/', httponly=False, secure=request.is_secure, samesite='Strict', expires=exp)
	return res

# todo: add renew route to refresh the session token if it is close to expiring

# consider adding facebook if google auth is not enough
# https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow
# https://developers.facebook.com/docs/facebook-login/limited-login/

@bp.route('/logout', methods=['POST'])
def logout():
	res = make_response(success_json())
	res.set_cookie('session_token', '', expires=0, path='/')
	return res