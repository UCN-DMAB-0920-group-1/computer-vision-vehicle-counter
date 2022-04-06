import json
from logging import exception

from flask import Config


class Configuration(dict):
    __instance = None

    @staticmethod
    def get(key: str):
        """ Static access method. """
        if Configuration.__instance == None:
            Configuration()

        keys = key.split(".")

        if(len(keys) == 1):
            return Configuration.__instance.env[key]
        else:
            conf_map = Configuration.__instance.env
            for new_key in keys:
                if(new_key is None or new_key is ""):
                    raise Exception(
                        "${new_key} is empty! thats illegal! full key: ${key}")

                conf_map = conf_map[new_key]
            return conf_map

    def __init__(self):
        """ Virtually private constructor. """
        if Configuration.__instance != None:
            raise Exception("This class is a Configuration!")
        else:
            Configuration.__instance = self
            with open("api/conf.json", "r") as config:
                self.env = json.load(config)


# USE AS:
# Configuration.get("SECRET_KEY")
# Configuration.get("APP_SETTINGS.MAX_THREADS")
