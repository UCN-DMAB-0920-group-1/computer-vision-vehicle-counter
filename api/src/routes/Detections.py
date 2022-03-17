from time import sleep
from tracking_module.tracking import Tracking
from dao.dao_detections import dao_detections
from flask import abort, jsonify, send_from_directory
import uuid
import os
import threading


class Detections:

    def __init__(self, thread_list: list, UPLOAD_FOLDER: str,
                 Tracking: Tracking, dao_detections: dao_detections, MAX_THREADS: int):

        self.thread_list = thread_list
        self.MAX_THREADS = MAX_THREADS
        self.task_queue = []
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.Tracking = Tracking
        self.dao_detections = dao_detections

    def upload_video(self, request):
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

        id = str(uuid.uuid4())
        video_path = os.path.join(self.UPLOAD_FOLDER, (id + ".mp4"))
        file.save(video_path)

        threadCount = self.checkThreadCount()
        if threadCount >= self.MAX_THREADS:
            task = {"video_path": video_path, "id": id}
            self.task_queue.append(task)
            return abort(
                503, 'Task added to queue, check result again latorz. you are number:' +
                str(len(self.task_queue)))
        try:
            self.startVideoTracker(id, video_path)
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

    def startVideoTracker(self, id, video_path):
        thread = threading.Thread(target=self.threadVideoTracker,
                                  args=(id, video_path),
                                  daemon=True)
        self.thread_list.append(thread)
        thread.start()
        return "Thread started"

    def threadVideoTracker(self, id, video_path):
        try:
            tracker = self.Tracking(should_draw=True,
                                    roi_area=[[(100, 400), (100, 200),
                                               (600, 200), (600, 487)]])
            detections = tracker.track(video_path)
            res = self.dao_detections.insert_one(id, detections)
        except Exception as e:
            print(e)
        finally:
            os.remove(video_path)
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

    def checkQueue(self):
        print("Checking task list...")
        if self.checkThreadCount() < self.MAX_THREADS and len(self.task_queue) > 0:
            print("Starting new task")
            task = self.task_queue.pop(0)
            self.startVideoTracker(task["id"], task["video_path"])
        return len(self.task_queue)
