
from flask import abort, jsonify
import json
import os
import threading
import uuid
from ..pusher_socket import PusherSocket
from ..interfaces.i_filehandler import IFileHandler
from ..interfaces.i_tracker import ITracker
from ..DAO.dao_detections import DaoDetections
from ..model.task import Task


class Detections:

    def __init__(self, UPLOAD_FOLDER: str, STORAGE_FOLDER: str,
                 tracker: ITracker, dao_detections: DaoDetections,
                 MAX_THREADS: int, ALLOWED_EXTENSIONS: set[str],
                 filehandler: IFileHandler):

        self.filehandler = filehandler
        self.thread_list: list[threading.Thread] = []
        self.task_queue: list[Task] = []
        self.MAX_THREADS = MAX_THREADS
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.STORAGE_FOLDER = STORAGE_FOLDER
        self.ALLOWED_EXTENSIONS: set[str] = ALLOWED_EXTENSIONS
        self.tracker: ITracker = tracker
        self.dao_detections: DaoDetections = dao_detections

    def upload_video(self, request, UUID):
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
        temp_video_path = os.path.join(self.STORAGE_FOLDER, (id + ".mp4"))
        file = request.files['file']
        self.save_video_file(temp_video_path, file)

        # Add pending task to database
        self.dao_detections.insert_one_task(id, "Pending", UUID)

        socket = PusherSocket("private-video-channel-" + UUID)

        socket.send_notification("video-event", {
            "status": "Pending",
            "id": id
        })

        threadCount = self.checkThreadCount()
        if threadCount >= self.MAX_THREADS:

            task = Task(id, temp_video_path, options, bbox, UUID)

            self.task_queue.append(task)
            return abort(
                503,
                'Task added to queue, check result again latorz. you are number:'
                + str(len(self.task_queue)))
        try:
            self.startVideoTracker(id, temp_video_path, options, bbox, UUID)
        except Exception as e:
            print("Exception while starting detection and tracker" + str(e))
            return abort(
                500, 'Internal error while starting video task, try again')
        return jsonify({'id': id})

    def get_video(self, uuid, videoId):

        # Next lines below might need to be moved into IStorageHandler
        # filename = videoId + ".mp4"
        # filename += "_processed.mkv"

        return self.filehandler.download(uuid, videoId)

    def get_count(self, id):
        res = self.dao_detections.find_one(id)
        return jsonify(res)

    def get_user_videos(self, UUID):
        res = self.dao_detections.find(key="UUID", value=UUID)
        return jsonify(res)

    ############# - METHODS - #############

    def startVideoTracker(self, id, temp_video_path, options: map, bbox, UUID):
        thread = threading.Thread(target=self.threadVideoTracker,
                                  args=(id, temp_video_path, options, bbox,
                                        UUID),
                                  daemon=True)
        self.thread_list.append(thread)
        thread.start()
        print("Thread Started: " + thread.getName())
        return "Thread started"

    def threadVideoTracker(self, id, video_path, options: map, bbox, UUID):
        if options['enabled'] == 'false':
            bbox = None
            max_distance_between_points = float(20)
            confidence = 0.6
        else:
            if len(bbox) == 0:
                # Create a proper fix for this (np array to np aray bug @bukz, @midi)
                bbox = None
            confidence = float(options['confidence'])
            max_distance_between_points = float(
                options['max_distance_between_points'])
        try:
            tracker = self.tracker(
                should_draw=True,
                confidence_threshold=confidence,
                max_distance_between_points=max_distance_between_points)

            detections = tracker.track(video_path, roi=bbox)

            path = video_path + "_processed.mkv"

            self.send_to_storage(path, UUID, id)

            self.dao_detections.update_one(id, detections)

            socket = PusherSocket("private-video-channel-" + UUID)
            socket.send_notification("video-event", {
                "status": "Finished",
                "id": id,
                "detections": detections
            })

        except Exception as e:
            print("EXCEPTION thrown in thread from threadVideoTracker:")
            print(e)

        finally:
            # Delete temp files
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(path):
                os.remove(path)

            print("Thread Done")
            self.check_queue()
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
            os.mkdir(self.STORAGE_FOLDER)
        except FileExistsError as e:
            print("path already exists")

        file.save(video_path)
        return "File saved"

    def check_queue(self):
        print("Checking task list...")

        if self.checkThreadCount() < self.MAX_THREADS + 1 and len(
                self.task_queue) > 0:
            print("Starting new task")
            task = self.task_queue.pop(0)
            self.startVideoTracker(task.id, task.video_path, task.options,
                                   task.bbox, task.UUID)
        return len(self.task_queue)

    def send_to_storage(self, path: str, UUID: int, id: str):
        try:
            # opening for [r]eading as [b]inary
            in_file = open(path, "rb")
            bytes = in_file.read()
            in_file.close()

            self.filehandler.upload(UUID + "/" + id + ".mkv", bytes)
        except Exception as e:
            print("could not save file" + str(e))
