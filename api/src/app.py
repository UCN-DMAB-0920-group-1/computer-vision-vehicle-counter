import os
import uuid
import threading
from flask import Flask, jsonify, flash, request, redirect, url_for, send_file, send_from_directory, safe_join, abort
from dao.daoDetections import daoDetections

from tracking_module.tracking import Tracking

app = Flask(__name__)
app.secret_key = "super secret key"
UPLOAD_FOLDER = '../storage/'  # check if working, this changes often!
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/video', methods=['POST'])
def upload_video():
    # check if the post request has the file part
    if 'file' not in request.files:
        return abort(404, 'No file part')
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return abort(404, 'No selected file')
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4())
        video_path = os.path.join(UPLOAD_FOLDER, (filename + ".mp4"))
        file.save(video_path)
        if threading.active_count() < 10:
            thread = threading.Thread(
                target=threadVideoTracker, args=(filename, video_path))
            thread.start()
            return jsonify({'id': filename})
        else:
            return abort(503, 'Queue is full, try again latorz count:' + str(threading.active_count()))
        # return jsonify({'id': res.inserted_id, "cars": detections['total']})


@app.route('/video/<string:id>/download')
def get_video(id):
    path = id + ".mp4"
    return send_from_directory(UPLOAD_FOLDER, path)  # mp4 is hardcoded


@app.route('/video/<string:id>')
def get_count(id):
    res = daoDetections.find_one(id)
    return jsonify(res)


def threadVideoTracker(filename, video_path):
    tracker = Tracking(should_draw=True,
                       roi_area=[(100, 400), (100, 200), (600, 200),
                                 (600, 487)])
    detections = tracker.track(video_path)
    res = daoDetections.insert_one(filename, detections)
    return
