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
from routes.Auth import Authenticator

# Load config
with open("api/conf.json", "r") as config:
    environment = json.load(config)

thread_list = []
app = Flask(__name__)
app.secret_key = environment["SECRET_KEY"]
cors = CORS(app, resources={r"*": {"origins": "*"}})

UPLOAD_FOLDER = 'api/storage/'  # check if working, this changes often!
ALLOWED_EXTENSIONS = {'mp4'}
MAX_THREADS = 4
CLIENT_ID = '512124053214-vpk9p42i9ls413asejsa9bg7j1b4nq61.apps.googleusercontent.com'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# detections routes init
_detections = Detections(thread_list, UPLOAD_FOLDER, Tracking, dao_detections,
                         MAX_THREADS)

_authenticator = Authenticator(CLIENT_ID, app.secret_key,
                               environment["JWT_algorithm"],
                               environment["CLIENT_SECRET"])
############# - ROUTES - #############


@app.route('/detection', methods=['POST'])
def upload_video():
    return _detections.upload_video(request)


@app.route('/detection/<string:id>/video')
def get_video(id):
    return _detections.get_video(id)


@app.route('/detection/<string:id>')
def get_count(id):
    return _detections.get_count(id)


@app.route('/auth', methods=["POST"])
def auth():
    res = _authenticator.authenticate_google(request)
    if res == False: return Response("Failed to authenticate user", 401)
    return Response("Succes", 200, {"jwt": res})


@app.route("/auth", methods=["GET"])
def login():
    code = request.args.get('code')
    #returns empty string if failed to authenticate
    res = _authenticator.authenticate_google(code)

    return jsonify({"jwt": res})


#