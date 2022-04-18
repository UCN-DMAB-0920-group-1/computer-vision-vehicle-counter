from abc import ABC, abstractmethod


class IFileHandler(ABC):
    @abstractmethod
    def upload(self, path: str, bytes):
        pass

    @abstractmethod
    def download(self, dir: str, path: str):
        pass

    @abstractmethod
    def delete(self, path: str):
        pass
