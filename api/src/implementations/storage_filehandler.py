import os
from flask import send_from_directory
from src.filehandler_module.infrastructure.i_filehandler import IFileHandler


class StorageFilehandler(IFileHandler):
    def upload(self, path, bytes):
        with open(path, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(bytes)

    def download(self, dir, filename):
        send_from_directory(dir, filename)  # mp4 is hardcoded

    def delete(self, path):
        os.remove(path)


if __name__ == '__main__':
    StorageFilehandler()
