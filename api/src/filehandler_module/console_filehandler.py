from infrastructure.i_filehandler import IFileHandler


class ConsoleFilehandler(IFileHandler):
    def upload(self, path, bytes):
        print("going to upload file at " + path)

    def download(self, dir, path):
        print("going to download file at " + dir + "\\" + path)

    def delete(self, path):
        print("going to delete file at " + path)


if __name__ == '__main__':
    ConsoleFilehandler()
