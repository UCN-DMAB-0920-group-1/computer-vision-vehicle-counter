class Task:
    def __init__(self, id: str, video_path: str, options: map, bbox, UUID: str):
        self.id = id
        self.options = options
        self.video_path = video_path
        self.bbox = bbox
        self.UUID = UUID
