from abc import ABC, abstractmethod


class IFileHandler(ABC):
    @abstractmethod
    def upload(self, path, bytes):
        pass

    @abstractmethod
    def download(self, dir, path):
        pass

    @abstractmethod
    def delete(self, path):
        pass
