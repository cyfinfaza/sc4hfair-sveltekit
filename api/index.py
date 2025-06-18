from flask import Flask, Blueprint
from flask_cors import CORS
import dotenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.update(
	SESSION_COOKIE_NAME='pvt_s',
	SESSION_COOKIE_SAMESITE='None',
	SESSION_COOKIE_SECURE=True,
	SECRET_KEY='--------' # DO NOT CHANGE THIS UNLESS YOU WANT ALL REGISTERED SESSIONS TO BREAK
)
CORS(app, origins=['*'], supports_credentials=True)

dotenv.load_dotenv()

bp = Blueprint('api', __name__, url_prefix='/api')

# for vercel to not create extra functions, every python file must start with an underscore
from . import _auth, _interests, _profile, _pvt, _scheduledNotifications, _webpush
bp.register_blueprint(_auth.bp)
bp.register_blueprint(_interests.bp)
bp.register_blueprint(_profile.bp)
bp.register_blueprint(_pvt.bp)
bp.register_blueprint(_scheduledNotifications.bp)
bp.register_blueprint(_webpush.bp)

app.register_blueprint(bp)

if __name__ == '__main__':
	app.run(debug=True, port=6002)
