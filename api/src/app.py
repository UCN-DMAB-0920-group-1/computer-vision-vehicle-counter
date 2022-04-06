import json
from os import abort
import uuid
from tracking_module.util import get_payload_from_jwt
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from dao.dao_detections import DaoDetections
from routes.Detections import Detections
from tracking_module.tracking import Tracking
from pusher_socket import PusherSocket
from routes.Auth import Authenticator

# Load config
with open("api/conf.json", "r") as config:
    environment = json.load(config)

app = Flask(__name__)
app.secret_key = environment["SECRET_KEY"]
MAX_THREADS = environment["APP_SETTINGS"]["MAX_THREADS"]
UPLOAD_FOLDER = environment["APP_SETTINGS"]["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = set(environment["APP_SETTINGS"]["ALLOWED_EXTENSIONS"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"*": {"origins": "*"}})
# detections routes init
_detections = Detections(UPLOAD_FOLDER, Tracking, DaoDetections, MAX_THREADS,
                         ALLOWED_EXTENSIONS)


_authenticator = Authenticator(
    environment["CLIENT_ID"], app.secret_key,
    environment["JWT_algorithm"],
    environment["CLIENT_SECRET"]
)

############# - ROUTES - #############


@app.route('/detection', methods=['POST'])
def upload_video():
    permitted = _authenticator.checkPermission(request)
    UUID = get_payload_from_jwt(request, "UUID", app.secret_key)
    return _detections.upload_video(
        request,
        UUID) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>/video')
def get_video(id):
    permitted = _authenticator.checkPermission(request)
    return _detections.get_video(
        id) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>')
def get_count(id):
    permitted = _authenticator.checkPermission(request)
    return _detections.get_count(
        id) if permitted else "Not permitted to access this resource"


@app.route('/detection/user')
def get_user_videos():
    UUID = request.args.get("UUID")
    print(UUID)
    permitted = _authenticator.checkPermission(request)
    return _detections.get_user_videos(
        UUID) if permitted else "Not permitted to access this resource"
    pass


@app.route("/auth", methods=["GET"])
def login():
    code = request.args.get('code')
    # returns empty string if failed to authenticate
    res = _authenticator.authenticate_google(code)
    print(res)
    return jsonify({"jwt": res})


@app.route('/auth/pusher', methods=['POST'])
def pusher_auth():
    res = _authenticator.authenticate_pusher(request)

    if(res == 401):
        return abort(401, "unauthenticated")

    return res
