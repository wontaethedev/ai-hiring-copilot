import aioboto3
import asyncio


class S3Handler:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
        s3_bucket_name: str,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        try:
            self.session = aioboto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
        except Exception as e:
            raise Exception(f"Failed to create AWS S3 session | {str(e)}")
        self.s3_bucket_name = s3_bucket_name

    async def upload_file(self, local_file_path: str, object_key: str) -> None:
        """
        Upload a file to the S3 bucket
        """

        async with self.session.client("s3") as s3:
            try:
                await s3.upload_file(local_file_path, self.s3_bucket_name, object_key)
            except Exception as e:
                raise Exception(
                    f"Failed to upload the file {local_file_path} to S3 bucket | {str(e)}"
                )

    async def batch_upload_files(self, files: list[tuple[str, str]]) -> None:
        """
        Upload a batch of files to the S3 bucket concurrently
        """

        tasks = []
        for local_path, object_key in files:
            tasks.append(self.upload_file(local_path, object_key))

        await asyncio.gather(*tasks)

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
