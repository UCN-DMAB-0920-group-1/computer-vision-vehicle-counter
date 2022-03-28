import os
from time import strftime, strptime
import uuid
import threading
from flask import Flask, jsonify, flash, request, redirect, url_for, send_file, send_from_directory, safe_join, abort
from flask_cors import CORS
from dao.dao_detections import dao_detections
from routes.Detections import Detections
from tracking_module.tracking import Tracking
from google.oauth2 import id_token
from google.auth.transport import requests

thread_list = []
app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app, resources={r"*": {"origins": "*"}})

UPLOAD_FOLDER = 'api/storage/'  # check if working, this changes often!
ALLOWED_EXTENSIONS = {'mp4'}
MAX_THREADS = 4
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# detections routes init
detections = Detections(thread_list, UPLOAD_FOLDER,
                        Tracking, dao_detections, MAX_THREADS)

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


@app.route('/auth', methods=["POST", "GET"])
def auth():
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU4YjQyOTY2MmRiMDc4NmYyZWZlZmUxM2MxZWIxMmEyOGRjNDQyZDAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MTIxMjQwNTMyMTQtdnBrOXA0Mmk5bHM0MTNhc2Vqc2E5Ymc3ajFiNG5xNjEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MTIxMjQwNTMyMTQtdnBrOXA0Mmk5bHM0MTNhc2Vqc2E5Ymc3ajFiNG5xNjEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDAwNDEyMTg4Mjk3ODI2NTM0NzciLCJhdF9oYXNoIjoiQ2Q2QVc5eHB0SDZWRTdrdGx3ZlRoZyIsIm5vbmNlIjoiMDM5NDg1Mi0zMTkwNDg1LTI0OTAzNTgiLCJpYXQiOjE2NDg0NjYwODAsImV4cCI6MTY0ODQ2OTY4MCwianRpIjoiMzk2OTdiYjdmOTlhMmEyM2QyMGMwNzk1OGQ5YjI2MTIxYjhkOGFkMiJ9.kuPT7CyxDidBV5_r6s7hLPsZs_lMi0udDkK5COCML8r8SLfYxEExowbtLzCVz7fE5Ojr3qu4whNssJxLAOJ5QCUoc6I3A3x9qMqYc6bVTOEKjDPQknOfQZU1YKkQIdQm_v4k4-zRgvsmb2JbN3iPbNn1Z0liLCgvEOKjmhqc9ENzhLu2w2weEMrRlRnCIsRbM_enx7pBiFHk8rz8cG_7xYwcM2ivmFQ-gmaNUc2UUOsCh4Z5xik8dXuLgEVadLJ_FZ5s0qGRlcyNcEFrt0O86u8Iteq8gEJZN9YQFSJ7k1bRNsV73shILh19oUanaAeuovUJb87IPNcfY6ot46510g'
    CLIENT_ID = '512124053214-vpk9p42i9ls413asejsa9bg7j1b4nq61.apps.googleusercontent.com'
    res = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return jsonify(res)
