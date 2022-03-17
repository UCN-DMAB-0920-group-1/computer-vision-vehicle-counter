class IDao:

    def find_one(id: int):  #should read a single object
        pass

    def insert_one(id: int, object):  #should insert one object with id as key
        pass

    def delete_one(id: int):  #should delete one object with id
        pass

    def update_one(id: int, object):  #should update object with id
        pass

    def insert_many(
        object: dict
    ):  #should insert all objects with key as id and value as object
        pass