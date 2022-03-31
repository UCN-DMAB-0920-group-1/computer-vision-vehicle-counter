from src.dao.dao_detections import dao_detections
from src.routes.detections import Detections
from src.tracking_module.tracking import Tracking
from flask import Flask, request
from flask_cors import CORS

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
