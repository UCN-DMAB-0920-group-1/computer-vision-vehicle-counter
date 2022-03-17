from tracking_module.tracking import Tracking
from dao.dao_detections import dao_detections
from flask import abort, jsonify, send_from_directory
import uuid
import os
import threading


class Detections:

    def __init__(self, thread_list: list, UPLOAD_FOLDER: str,
                 Tracking: Tracking, dao_detections: dao_detections):

        self.thread_list = thread_list
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.Tracking = Tracking
        self.dao_detections = dao_detections

    def upload_video(self, request):
        self.validate_video_post(request)
        file = request.files['file']
        options = {
            'enabled': request.form['enabled'],
            'startX': request.form['startX'],
            'endX': request.form['endX'],
            'startY': request.form['startY'],
            'endY': request.form['endY'],
            'confidence': request.form['confidence']
        }
        id = str(uuid.uuid4())
        video_path = os.path.join(self.UPLOAD_FOLDER, (id + ".mp4"))
        file.save(video_path)
        try:
            thread = threading.Thread(target=self.threadVideoTracker,
                                      args=(id, video_path, options),
                                      daemon=True)
            self.thread_list.append(thread)
            thread.start()
        except Exception as e:
            print(e)
            return abort(
                500, 'Internal error while starting video task, try again')
        return jsonify({'id': id})

    def get_video(self, id):
        path = id + ".mp4"
        return send_from_directory(self.UPLOAD_FOLDER,
                                   path)  # mp4 is hardcoded

    def get_count(self, id):
        res = self.dao_detections.find_one(id)
        return jsonify(res)

    ############# - METHODS - #############

    def threadVideoTracker(self, id, video_path, options: map):
        if options['enabled'] == 'false':
            roi = [[(0, 0), (1920, 0), (1920, 1080), (0, 1080)]]
            confidence = 0.6
        else:
            roi = [[(options['startX'], options['startY']),
                    (options['endX'], options['startY']),
                    (options['endX'], options['endY']),
                    (options['startX'], options['endY'])]]
            confidence = options['confidence']

        try:
            tracker = self.Tracking(should_draw=True,
                                    roi_area=roi,
                                    confidence_threshold=confidence)
            detections = tracker.track(video_path)
            res = self.dao_detections.insert_one(id, detections)
        except Exception as e:
            print(e)
        finally:
            os.remove(video_path)
            return 'Thread Done'

    def checkThreadCount(self):
        count = 0
        for t in self.thread_list:
            if t.is_alive():
                count += 1
        print('Threads running: ' + str(count))
        return count

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def validate_video_post(self, request):

        # check if the post request has the file part
        if 'file' not in request.files:
            return abort(404, 'No file part')
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return abort(404, 'No selected file')

        if not file and not self.allowed_file(file.filename):
            return abort(403, 'File is not allowed to be uploaded')

        threadCount = self.checkThreadCount()
        if threadCount > 2:
            return abort(
                503, 'Queue is full, try again latorz. Job count:' +
                str(threadCount))