from abc import ABC, abstractmethod


class IDao(ABC):
    @abstractmethod
    def find_one(id: int):  # should read a single object
        pass

    @abstractmethod
    def insert_one(id: int, object):  # should insert one object with id as key
        pass

    @abstractmethod
    def delete_one(id: int):  # should delete one object with id
        pass

    @abstractmethod
    def update_one(id: int, object):  # should update object with id
        pass

    @abstractmethod
    def insert_many(
        object: dict
    ):  # should insert all objects with key as id and value as object
        pass
