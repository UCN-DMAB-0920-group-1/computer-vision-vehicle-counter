from abc import ABC, abstractmethod


class IDaoDetections(ABC):
    @abstractmethod
    def find(key: str, value):  # should read a single object
        pass

    @abstractmethod
    def find_one(id: str):  # should read a single object
        pass

    @abstractmethod
    def insert_one(id: str, object):  # should insert one object with id as key
        pass

    @abstractmethod
    def delete_one(id: str):  # should delete one object with id
        pass

    @abstractmethod
    def update_one(id: str, object):  # should update object with id
        pass

    @abstractmethod
    def insert_many(
        object: dict
    ):  # should insert all objects with key as id and value as object
        pass
