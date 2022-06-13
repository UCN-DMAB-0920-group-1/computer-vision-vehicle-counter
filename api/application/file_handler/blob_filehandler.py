import os
from flask import send_from_directory

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from ..interfaces.i_filehandler import IFileHandler
from configuration import Configuration


class BlobFilehandler(IFileHandler):

    def upload(self, path, bytes):
        container_name = path.split("/")[0]
        blob_name = path.split("/")[1]

        container_client = ContainerClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=container_name)

        if not container_client.exists():
            container_client.create_container()

        blob = BlobClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=container_name,
            blob_name=blob_name)

        blob.upload_blob(bytes)

    def download(self, dir, filename):
        filename = filename + ".mkv"
        blob = BlobClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=dir,
            blob_name=filename)

        path = Configuration.ROOT_DIR + "/" + Configuration.get(
            "APP_SETTINGS.STORAGE_FOLDER")

        print("PATH: " + path)
        with open(f"{path}/{filename}", "wb+") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)

        return send_from_directory(path, filename)

    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
