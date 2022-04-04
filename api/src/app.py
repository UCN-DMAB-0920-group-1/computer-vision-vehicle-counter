import json
import os
from time import strftime, strptime
import uuid
import threading
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from dao.dao_detections import dao_detections
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
# {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"*": {"origins": "*"}})
# detections routes init
_detections = Detections(UPLOAD_FOLDER, Tracking, dao_detections,
                         MAX_THREADS, ALLOWED_EXTENSIONS)

_authenticator = Authenticator(environment["CLIENT_ID"], app.secret_key,
                               environment["JWT_algorithm"],
                               environment["CLIENT_SECRET"])
############# - ROUTES - #############


@app.route('/detection', methods=['POST'])
def upload_video():
    permitted = checkPermission(request)
    return _detections.upload_video(
        request) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>/video')
def get_video(id):
    permitted = checkPermission(request)
    return _detections.get_video(
        id) if permitted else "Not permitted to access this resource"


@app.route('/detection/<string:id>')
def get_count(id):
    permitted = checkPermission(request)
    return _detections.get_count(
        id) if permitted else "Not permitted to access this resource"


@app.route('/pusher/<string:toSend>', methods=['GET'])
def pusher_test(toSend):
    socket = PusherSocket("my-channel")
    socket.send_notification("my-event", {"message": "123321"})
    return "Send!"


@app.route("/auth", methods=["GET"])
def login():
    code = request.args.get('code')
    # returns empty string if failed to authenticate
    res = _authenticator.authenticate_google(code)
    print(res)
    return jsonify({"jwt": res})

######### METHODS #########


def checkPermission(request):
    res = False
    if "Authorization" in request.headers:
        # decoes JWT and looks at payload value "valid" return true if succes and false if not
        res = _authenticator.authenticate_JWT(request.headers["Authorization"])
    return res
