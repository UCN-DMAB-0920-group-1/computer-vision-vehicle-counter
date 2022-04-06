from infrastructure.i_filehandler import IFileHandler


class StorageFilehandler(IFileHandler):
    def upload(self, path, bytes):
        print("going to upload file at " + path)

    def download(self, dir, filename):
        send_from_directory(dir, filename)  # mp4 is hardcoded

    def delete(self, path):
        os.remove(path)


if __name__ == '__main__':
    StorageFilehandler()
