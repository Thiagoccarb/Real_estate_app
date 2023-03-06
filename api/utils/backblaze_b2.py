import os
import uuid
import b2sdk.v1 as b2
from dotenv import load_dotenv


load_dotenv()

info = b2.InMemoryAccountInfo()
b2_api = b2.B2Api(info)

application_key_id = os.getenv("B2_KEY_ID")
application_key = os.getenv("B2_APPLICATION_KEY")
bucket_name = os.getenv("BUCKET_NAME")
cluster_number = os.getenv("B2_CLUSTER_NUMBER")

class B2skd():

    def __init__(self) -> None:
        self.__application_key_id = application_key_id
        self.__application_key = application_key
        self.__bucket_name = bucket_name
        self.__cluster_number = cluster_number
        self.__filename = self.__create_file_name()
    
    
    def __create_file_name(self) -> str:
        return str(uuid.uuid4())

   
    def upload_binary_to_blackblaze(self, binary: bytes) -> None:
        b2_api.authorize_account("production", self.__application_key_id, self.__application_key)
        bucket = b2_api.get_bucket_by_name(self.__bucket_name)
        bucket.upload_bytes(binary, self.__filename)



    def get_download_url(self) -> str:
        return f"https://f{self.__cluster_number}.backblazeb2.com/file/{self.__bucket_name}/{self.__filename}"
