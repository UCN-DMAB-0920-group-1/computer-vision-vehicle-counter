from time import sleep
from tracking_module.tracking import Tracking
from dao.dao_detections import dao_detections
from flask import abort, jsonify, send_from_directory
import json
import uuid
import os
import threading


class Detections:

    def __init__(self, thread_list: list, UPLOAD_FOLDER: str,
                 Tracking: Tracking, dao_detections: dao_detections,
                 MAX_THREADS: int):

        self.thread_list = thread_list
        self.MAX_THREADS = MAX_THREADS
        self.task_queue = []
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.Tracking = Tracking
        self.dao_detections = dao_detections

    def upload_video(self, request):
        self.validate_video_post(request)
        file = request.files['file']

        options = {
            'enabled':
            request.form['enabled'],
            'confidence':
            request.form['confidence'],
            'max_distance_between_points':
            request.form['maxDistanceBetweenPoints'],
        }

        bbox = json.loads(request.form["bbox"])

        id = str(uuid.uuid4())
        video_path = os.path.join(self.UPLOAD_FOLDER, (id + ".mp4"))
        file = request.files['file']
        self.save_video_file(video_path, file)
        # Add pending task to database
        self.dao_detections.insert_one_task(id, "Pending")

        threadCount = self.checkThreadCount()
        if threadCount >= self.MAX_THREADS:

            task = Task(id, video_path, options, bbox)

            self.task_queue.append(task)
            return abort(
                503,
                'Task added to queue, check result again latorz. you are number:'
                + str(len(self.task_queue)))
        try:
            self.startVideoTracker(id, video_path, options, bbox)
        except Exception as e:
            print("Exception in uploading video: " + str(e))
            return abort(
                500, 'Internal error while starting video task, try again')
        return jsonify({'id': id})

    def get_video(self, id):
        path = id + ".mp4"
        path += "_processed.mkv"
        return send_from_directory(self.UPLOAD_FOLDER,
                                   path)  # mp4 is hardcoded

    def get_count(self, id):
        res = self.dao_detections.find_one(id)
        return jsonify(res)

    ############# - METHODS - #############

    def startVideoTracker(self, id, video_path, options: map, bbox):
        thread = threading.Thread(target=self.threadVideoTracker,
                                  args=(id, video_path, options, bbox),
                                  daemon=True)
        self.thread_list.append(thread)
        thread.start()
        print("Thread Started: " + thread.getName())
        return "Thread started"

    def threadVideoTracker(self, id, video_path, options: map, bbox):
        if options['enabled'] == 'false':
            bbox = [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]
            confidence = 0.6
        else:
            if len(bbox) == 0:
                bbox = [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]
            confidence = float(options['confidence'])
            max_distance_between_points = float(
                options['max_distance_between_points'])
        try:
            tracker = self.Tracking(
                should_draw=True,
                roi_area=bbox,
                confidence_threshold=confidence,
                max_distance_between_points=max_distance_between_points)

            detections = tracker.track(video_path)
            self.dao_detections.update_one_task(id, detections)

        except Exception as e:
            print("EXCEPTION in thread: " + str(e))

        finally:
            os.remove(video_path)

            print("Thread Done")
            self.checkQueue()
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

        if request.content_length > 1000000000:
            return abort(403, 'File is too large - try a smaller video')

    def create_options(self, request):
        if 'enabled' not in request.form:
            return {'enabled': 'false'}
        return {
            'enabled': request.form['enabled'],
            'startX': request.form['startX'],
            'endX': request.form['endX'],
            'startY': request.form['startY'],
            'endY': request.form['endY'],
            'confidence': request.form['confidence']
        }

    def save_video_file(self, video_path, file):
        try:
            os.mkdir(self.UPLOAD_FOLDER)
        except FileExistsError as e:
            print("path already exists")

        file.save(video_path)
        return "File saved"

    def checkQueue(self):
        print("Checking task list...")
        if self.checkThreadCount() < self.MAX_THREADS and len(
                self.task_queue) > 0:
            print("Starting new task")
            task = self.task_queue.pop(0)
            self.startVideoTracker(task.id, task.video_path, task.options,
                                   task.bbox)
        return len(self.task_queue)


###### CLASSES #####


class Task:

    def __init__(self, id: str, video_path: str, options: map, bbox):
        self.id = id
        self.options = options
        self.video_path = video_path
        self.bbox = bbox
