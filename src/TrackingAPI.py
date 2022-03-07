import os
from flask import Flask, jsonify, flash, request, redirect, url_for, send_file, send_from_directory, safe_join, abort
from dummydata import dummydata
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super secret key"
test = dummydata()
UPLOAD_FOLDER = './sources'
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            return send_file('../sources/' + file.filename, as_attachment=True)
    return 'error'
