import os
from flask import send_from_directory
from src.filehandler_module.infrastructure.i_filehandler import IFileHandler
from src.configuration import Configuration


class StorageFilehandler(IFileHandler):
    def upload(self, path, bytes):
        os.mkdir(Configuration.getInstance(
        ).env["APP_SETTINGS"]["UPLOAD_FOLDER"])

        with open(path, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(bytes)

    def download(self, dir, filename):
        send_from_directory(dir, filename)

    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
