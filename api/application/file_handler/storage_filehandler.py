import os
from flask import send_from_directory
from interfaces.i_filehandler import IFileHandler
from configuration import Configuration

# used if you dont want to use blob storage and storage it local.


class StorageFilehandler(IFileHandler):
    # upload its with bytes
    def upload(self, path, bytes):
        # define what folder the file is going to be uploaded to
        os.mkdir(Configuration.get("APP_SETTINGS.UPLOAD_FOLDER"))
        # put the bytes in the path
        with open(path, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(bytes)
    # download from the local path

    def download(self, dir, filename):
        send_from_directory(dir, filename)
    # delete it from the local path

    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
