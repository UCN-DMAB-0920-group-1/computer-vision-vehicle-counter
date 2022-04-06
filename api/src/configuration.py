import json


class Configuration:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Configuration.__instance == None:
            Configuration()
        return Configuration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Configuration.__instance != None:
            raise Exception("This class is a Configuration!")
        else:
            Configuration.__instance = self
            with open("api/conf.json", "r") as config:
                self.env = json.load(config)
