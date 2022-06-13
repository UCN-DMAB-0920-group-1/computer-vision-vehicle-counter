from ..interfaces.i_filehandler import IFileHandler

# use interface IFillHandler


class ConsoleFilehandler(IFileHandler):
    # prints out the path
    def upload(self, path, bytes):
        print("going to upload file at " + path)
    # prints out the path and directory

    def download(self, dir, path):
        print("going to download file at " + dir + "\\" + path)
    # prints what path is going to be deleted

    def delete(self, path):
        print("going to delete file at " + path)
