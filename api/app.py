import json
import uuid
from pymongo import MongoClient

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from infrastructure.console_tracker import ConsoleTracker
from application.i_filehandler import IFileHandler
from configuration import Configuration

from infrastructure.dao_detections import DaoDetections
from infrastructure.routes.Auth import Authenticator
from infrastructure.routes.detections import Detections
from application.i_tracker import ITracker
from tracking_module.util import get_payload_from_jwt
from tracking_module.tracker import Tracker
from infrastructure.blob_filehandler import BlobFilehandler

# Load config
app = Flask(__name__)

SECRET_KEY = Configuration.get("SECRET_KEY")
MAX_THREADS = Configuration.get("APP_SETTINGS.MAX_THREADS")
TEMP_STORAGE_FOLDER = Configuration.get("APP_SETTINGS.STORAGE_FOLDER")
UPLOAD_FOLDER = Configuration.get("APP_SETTINGS.UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = set(Configuration.get("APP_SETTINGS.ALLOWED_EXTENSIONS"))

cors = CORS(app, resources={r"*": {"origins": "*"}})
# detections routes init
_filehandler: IFileHandler = BlobFilehandler()
_tracker: ITracker = Tracker

mongo_client = MongoClient(Configuration.get("mongodb"))

_detections = Detections(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    STORAGE_FOLDER=TEMP_STORAGE_FOLDER,
    tracker=_tracker,
    dao_detections=DaoDetections(mongoClient=mongo_client),
    MAX_THREADS=MAX_THREADS,
    ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS,
    filehandler=_filehandler)

_authenticator = Authenticator(Configuration.get("CLIENT_ID"), SECRET_KEY,
                               Configuration.get("JWT_algorithm"),
                               Configuration.get("CLIENT_SECRET"))

############# - ROUTES - #############


@app.route('/')
def index():
    return 'hello, world!'


@app.route('/detection', methods=['POST'])
def upload_video():
    permitted = _authenticator.check_permission(request)
    UUID = get_payload_from_jwt(request, "UUID", SECRET_KEY)
    return _detections.upload_video(
        request,
        UUID) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>/video')
def get_video(id):
    permitted = _authenticator.check_permission(request)
    UUID = get_payload_from_jwt(request, "UUID", SECRET_KEY)
    return _detections.get_video(
        UUID, id) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>')
def get_count(id):
    permitted = _authenticator.check_permission(request)
    return _detections.get_count(
        id) if permitted else "Not permitted to access this resource"


@app.route('/detection/user')
def get_user_videos():
    UUID = request.args.get("UUID")
    print(UUID)
    permitted = _authenticator.check_permission(request)
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

    if (res == 401):
        return abort(401, "unauthenticated")

    return res


if __name__ == '__main__':
    app.run()
