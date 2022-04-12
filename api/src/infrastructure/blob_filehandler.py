import os
from flask import send_from_directory

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from src.application.i_filehandler import IFileHandler
from configuration import Configuration


class BlobFilehandler(IFileHandler):

    def __init__(self):
        self.blob = BlobServiceClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"))

    def upload(self, path, bytes):
        container_name = path.split("/")[0]
        blob_name = path.split("/")[1]

        container_client = ContainerClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"), container_name=container_name)

        if not container_client.exists():
            container_client.create_container()

        blob = BlobClient.from_connection_string(conn_str=Configuration.get(
            "BLOB_STORAGE"), container_name=container_name, blob_name=blob_name)

        blob.upload_blob(bytes)

    def download(self, dir, filename):
        blob = BlobClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"), container_name=dir, blob_name=filename)

        path = Configuration.get(
            "APP_SETTINGS.STORAGE_FOLDER") + filename
        print("PATH: " + path)
        with open(path, "wb+") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)

        # TODO: maybe stream blob_data instead?
        send_from_directory("./" + Configuration.get(
            "APP_SETTINGS.STORAGE_FOLDER"), filename)

    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
