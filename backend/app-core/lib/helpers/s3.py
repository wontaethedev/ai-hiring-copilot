from typing import TypedDict
import boto3
from concurrent.futures import ThreadPoolExecutor


class FileUpload(TypedDict):
    local_file_path: str
    object_key: str


class S3Handler:
    def __init__(self):
        self.client = boto3.resource("s3")

    def upload_file(self, file_upload: FileUpload, bucket_name: str) -> None:
        """
        Upload a file to the S3 bucket
        """
        local_file_path = file_upload["local_file_path"]
        object_key = file_upload["object_key"]
        if not local_file_path or not object_key:
            raise ValueError(f"Missing keys in file_upload: {file_upload}")

        try:
            self.client.Bucket(bucket_name).upload_file(local_file_path, object_key)
        except Exception as e:
            raise Exception(
                f"Failed to upload the file {local_file_path} to S3 bucket | {str(e)}"
            )

    def batch_upload_files(
        self,
        file_uploads: list[FileUpload],
        bucket_name: str,
        max_sessions: int = 5,
    ) -> None:
        """
        Upload a batch of files to the S3 bucket
        """
        with ThreadPoolExecutor(max_workers=max_sessions) as executor:
            futures = []

            for file_upload in file_uploads:
                future = executor.submit(self.upload_file, file_upload, bucket_name)
                futures.append(future)

            for f in futures:
                f.result()

    def download_file(self):
        """
        Download a file from the S3 bucket
        """
        pass

    def generate_presigned_GET_URL(self):
        """
        Generate a presigned GET URL to the S3 bucket
        """
        pass

    def generate_presigned_POST_URL(self):
        """
        Generate a presigned POST URL to the S3 bucket
        """
        pass
