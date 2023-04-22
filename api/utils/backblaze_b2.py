import os
from typing import List
import b2sdk.v1 as b2
from dotenv import load_dotenv

from utils.hash_md5 import md5_encrypter


load_dotenv()

info = b2.InMemoryAccountInfo()
b2_api = b2.B2Api(info)

application_key_id = os.getenv("B2_KEY_ID")
application_key = os.getenv("B2_APPLICATION_KEY")
bucket_name = os.getenv("BUCKET_NAME")
cluster_number = os.getenv("B2_CLUSTER_NUMBER")


class B2skd:
    def __init__(self) -> None:
        self.__application_key_id = application_key_id
        self.__application_key = application_key
        self.__bucket_name = bucket_name
        self.__cluster_number = cluster_number
        b2_api.authorize_account(
            "production", self.__application_key_id, self.__application_key
        )
        self.__bucket = b2_api.get_bucket_by_name(self.__bucket_name)

        self.__filename = None

    def __create_file_name(self, binary: bytes) -> str:
        return md5_encrypter(binary)

    def upload_binary_to_blackblaze(self, binary: bytes) -> None:
        self.__filename = self.__create_file_name(binary)
        self.__bucket.upload_bytes(binary, self.__filename)

    def get_download_url(self) -> str:
        return f"https://f{self.__cluster_number}.backblazeb2.com/file/{self.__bucket_name}/{self.__filename}"

    def list_file_names(self) -> List[str]:
        data = list(self.__bucket.ls())
        return [item[0].file_name for item in data]

    def delete_file_by_audio_hash(self, file_name: str) -> None:
        for file_version_info in self.__bucket.list_file_versions(file_name=file_name):
            self.__bucket.delete_file_version(
                file_version_info.id_, file_version_info.file_name
            )
