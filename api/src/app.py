import os
from time import strftime, strptime
import uuid
import threading
from flask import Flask, request, Response
from flask_cors import CORS
from dao.dao_detections import dao_detections
from routes.Detections import Detections
from tracking_module.tracking import Tracking
from routes.Auth import Authenticator

thread_list = []
app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app, resources={r"*": {"origins": "*"}})

UPLOAD_FOLDER = 'api/storage/'  # check if working, this changes often!
ALLOWED_EXTENSIONS = {'mp4'}
MAX_THREADS = 4
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# detections routes init
detections = Detections(thread_list, UPLOAD_FOLDER, Tracking, dao_detections,
                        MAX_THREADS)

authenticator = Authenticator()
############# - ROUTES - #############


@app.route('/detection', methods=['POST'])
def upload_video():
    return detections.upload_video(request)


@app.route('/detection/<string:id>/video')
def get_video(id):
    return detections.get_video(id)


@app.route('/detection/<string:id>')
def get_count(id):
    return detections.get_count(id)


@app.route('/auth', methods=["POST"])
def auth():
    res = authenticator.authenticate(request)
    if res == False:
        return Response("Failed to authenticate user", 401)
    return ("Success", 200)
