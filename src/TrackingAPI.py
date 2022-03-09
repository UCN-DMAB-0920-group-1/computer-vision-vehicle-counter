import json
import os
import uuid
from flask import Flask, jsonify, flash, request, redirect, url_for, send_file, send_from_directory, safe_join, abort
from dummydata import dummydata
from werkzeug.utils import secure_filename

from tracking_module.tracking import Tracking
from tracking_module.streams import streams

app = Flask(__name__)
app.secret_key = "super secret key"
<<<<<<< Updated upstream:src/TrackingAPI.py
test = dummydata()
UPLOAD_FOLDER = './sources'  # check if working, this changes often!
=======
UPLOAD_FOLDER = '../storage/'  # check if working, this changes often!
>>>>>>> Stashed changes:api/src/app.py
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


<<<<<<< Updated upstream:src/TrackingAPI.py
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(video_path)

            tracker = Tracking(should_draw=True,
                               roi_area=[(100, 400), (100, 200), (600, 200),
                                         (600, 487)])
            detections = tracker.track(video_path)

            return "total cars detected: " + str(
                detections["total"]), send_file('../sources/' + file.filename,
                                                as_attachment=True)

    return 'error'
=======
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
        filename = str(uuid.uuid4()) + '.mp4'
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(video_path)

        tracker = Tracking(should_draw=True,
                           roi_area=[(100, 400), (100, 200), (600, 200),
                                     (600, 487)])

        detections = tracker.track(video_path)

        return jsonify({'path': filename})


@app.route('/video/<string:id>/video')
def get_video(id):
    return send_from_directory(UPLOAD_FOLDER, id)


@app.route('/video/<string:id>')
def get_count(id):
    path = os.path.join(UPLOAD_FOLDER, 'tempDB.json')
    with open(path, 'r') as file:
        data = json.load(file)
    return jsonify(data[id])
>>>>>>> Stashed changes:api/src/app.py
