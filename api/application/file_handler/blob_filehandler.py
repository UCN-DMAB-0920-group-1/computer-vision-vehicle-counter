import os
from flask import send_from_directory

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from ..interfaces.i_filehandler import IFileHandler
from configuration import Configuration

# class that use IFileHandler interfaces


class BlobFilehandler(IFileHandler):
    # upload function to blob storage, that take path and bytes/file.
    def upload(self, path, bytes):
        # defiene what container we storage our data in
        container_name = path.split("/")[0]

        # defiene what name it will be giving
        blob_name = path.split("/")[1]

        # making connection to blob storage by use the connectionstring from our config.
        container_client = ContainerClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=container_name)
        # if there is no container in the blobstorage, it will create one.
        if not container_client.exists():
            container_client.create_container()
        # when there is connection and there is a container we have acces to the blob storage.
        blob = BlobClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=container_name,
            blob_name=blob_name)
        # and we can make the upload
        blob.upload_blob(bytes)

    def download(self, dir, filename):
        # define filename on what file we have to download and format
        filename = filename + ".mkv"
        # making connection to the blob storage and directory where the files are storage
        blob = BlobClient.from_connection_string(
            conn_str=Configuration.get("BLOB_STORAGE"),
            container_name=dir,
            blob_name=filename)
        # give the path where to temp storage the file
        path = Configuration.ROOT_DIR + "/" + Configuration.get(
            "APP_SETTINGS.STORAGE_FOLDER")

        print("PATH: " + path)

        # downlaod it to our temp path
        with open(f"{path}/{filename}", "wb+") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)
        # and send the directory where you can download it from
        return send_from_directory(path, filename)

    def delete(self, path):
        # checks if there is a path on the api and removes it.
        if os.path.exists(path):
            os.remove(path)
