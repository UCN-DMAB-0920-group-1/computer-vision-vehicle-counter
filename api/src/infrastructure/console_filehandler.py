from src.domain.i_filehandler import IFileHandler


class ConsoleFilehandler(IFileHandler):
    def upload(self, path, bytes):
        logger.logEntry("going to upload file at " + path)

    def download(self, dir, path):
        logger.logEntry("going to download file at " + dir + "\\" + path)

    def delete(self, path):
        logger.logEntry("going to delete file at " + path)
