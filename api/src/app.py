import os
import uuid
import threading
from flask import Flask, jsonify, flash, request, redirect, url_for, send_file, send_from_directory, safe_join, abort
from flask_cors import CORS
from dao.daoDetections import daoDetections


from tracking_module.tracking import Tracking

global thread_list
thread_list = []
app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app, resources={r"*": {"origins": "*"}})


UPLOAD_FOLDER = '../storage/'  # check if working, this changes often!
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

############# - ROUTES - #############


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
    if not file and not allowed_file(file.filename):
        return abort(403, 'File is not allowed to be uploaded')

    threadCount = checkThreadCount()
    if threadCount > 2:
        return abort(503, 'Queue is full, try again latorz. Job count:' + str(threadCount))

    id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_FOLDER, (id + ".mp4"))
    file.save(video_path)
    try:
        thread = threading.Thread(
            target=threadVideoTracker, args=(id, video_path), daemon=True)
        thread_list.append(thread)
        thread.start()
    except Exception as e:
        print(e)
        return abort(500, 'Internal error while starting video task, try again')
    return jsonify({'id': id})


@app.route('/video/<string:id>/download')
def get_video(id):
    path = id + ".mp4"
    return send_from_directory(UPLOAD_FOLDER, path)  # mp4 is hardcoded


@app.route('/video/<string:id>')
def get_count(id):
    res = daoDetections.find_one(id)
    return jsonify(res)

############# - METHODS - #############


def threadVideoTracker(id, video_path):
    try:
        tracker = Tracking(should_draw=True,
                           roi_area=[(100, 400), (100, 200), (600, 200),
                                     (600, 487)])
        detections = tracker.track(video_path)
        res = daoDetections.insert_one(id, detections)
    except Exception as e:
        print(e)
    finally:
        return 'Thread Done'


def checkThreadCount():
    count = 0
    for t in thread_list:
        if t.is_alive():
            count += 1
    print('Threads running: ' + str(count))
    return count


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
