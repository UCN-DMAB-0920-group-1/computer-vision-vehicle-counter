import json
from pymongo import MongoClient

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from src.dao.dao_detections import DaoDetections
from src.routes.Auth import Authenticator
from src.routes.detections import Detections
from src.tracking_module.tracker import Tracker
from src.tracking_module.util import get_payload_from_jwt
from src.implementations.storage_filehandler import StorageFilehandler

# Load config
with open("api/conf.json", "r") as config:
    environment = json.load(config)

app = Flask(__name__)
app.secret_key = environment["SECRET_KEY"]
MAX_THREADS = environment["APP_SETTINGS"]["MAX_THREADS"]
TEMP_STORAGE_FOLDER = environment["APP_SETTINGS"]["STORAGE_FOLDER"]
UPLOAD_FOLDER = environment["APP_SETTINGS"]["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = set(environment["APP_SETTINGS"]["ALLOWED_EXTENSIONS"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"*": {"origins": "*"}})
# detections routes init
filehandler: StorageFilehandler = StorageFilehandler()

mongo_client = MongoClient(environment["mongodb"])

_detections = Detections(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    STORAGE_FOLDER=TEMP_STORAGE_FOLDER,
    tracker=Tracker,
    dao_detections=DaoDetections(mongoClient=mongo_client),
    MAX_THREADS=MAX_THREADS,
    ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS,
    filehandler=filehandler
)

_authenticator = Authenticator(
    environment["CLIENT_ID"], app.secret_key,
    environment["JWT_algorithm"],
    environment["CLIENT_SECRET"]
)

############# - ROUTES - #############


@ app.route('/detection', methods=['POST'])
def upload_video():
    permitted = _authenticator.checkPermission(request)
    UUID = get_payload_from_jwt(request, "UUID", app.secret_key)
    return _detections.upload_video(
        request,
        UUID) if permitted else "Not permitted to access this resource"


@ app.route('/detection/<string:id>/video')
def get_video(id):
    permitted = _authenticator.checkPermission(request)
    return _detections.get_video(
        id) if permitted else "Not permitted to access this resource"


@ app.route('/detection/<string:id>')
def get_count(id):
    permitted = _authenticator.checkPermission(request)
    return _detections.get_count(
        id) if permitted else "Not permitted to access this resource"


@ app.route('/detection/user')
def get_user_videos():
    UUID = request.args.get("UUID")
    print(UUID)
    permitted = _authenticator.checkPermission(request)
    return _detections.get_user_videos(
        UUID) if permitted else "Not permitted to access this resource"
    pass


@ app.route("/auth", methods=["GET"])
def login():
    code = request.args.get('code')
    # returns empty string if failed to authenticate
    res = _authenticator.authenticate_google(code)
    print(res)
    return jsonify({"jwt": res})


@ app.route('/auth/pusher', methods=['POST'])
def pusher_auth():
    res = _authenticator.authenticate_pusher(request)

    if(res == 401):
        return abort(401, "unauthenticated")

    return res
