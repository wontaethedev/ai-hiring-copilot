import aioboto3
import asyncio
from fastapi import File, Form, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class S3Handler:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region_name: str,
        s3_bucket_name: str,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name
        self.s3_bucket_name = s3_bucket_name
        try:
            self.session = aioboto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region_name,
            )
        except Exception as e:
            raise Exception(f"Failed to create AWS S3 session | {str(e)}")

    async def upload_file(
        self, file: UploadFile = File(...), s3_path: str = Form(...)
    ) -> None:
        """
        Upload a file to the S3 bucket
        """

        object_key = f"{s3_path}/{file.filename}"

        async with self.session.client("s3") as s3:
            try:
                await s3.upload_fileobj(file.file, self.s3_bucket_name, object_key)
            except Exception as e:
                raise Exception(
                    f"Failed to upload the file {file.filename} to S3 bucket"
                ) from e

    async def batch_upload_files(self, files: list[UploadFile], s3_path: str) -> list:
        """
        Upload a batch of files to the S3 bucket concurrently

        Returns:
          - failed_files: a list of files failed to upload
        """

        tasks = [self.upload_file(file, s3_path) for file in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        failed_files = []
        for file, result in zip(files, results):
            if isinstance(result, Exception):
                failed_files.append(file.filename)

        return failed_files

    async def download_file(
        self,
        s3_path: str,
        filename: str,
        chunk_size: int = 69 * 1024,
    ) -> StreamingResponse:
        """
        Download a file from the S3 bucket
        """

        object_key = f"{s3_path}/{filename}"

        async with self.session.client("s3") as s3:
            try:
                s3_object = await s3.get_object(
                    Bucket=self.s3_bucket_name, Key=object_key
                )
            except Exception as e:
                raise Exception(f"File not found in S3: {str(e)}")

        async def iterfile():
            while chunk := await s3_object["Body"].read(chunk_size):
                yield chunk

        return StreamingResponse(iterfile(), media_type="application/octet-stream")

    async def generate_presigned_GET_URL(
        self, object_name: str, expiration: int = 3600
    ) -> str:
        """
        Generate a presigned GET URL to the S3 bucket
        """

        async with self.session.client("s3") as s3:
            try:
                url = await s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.s3_bucket_name, "Key": object_name},
                    ExpiresIn=expiration,
                )
            except Exception as e:
                raise Exception(
                    f"Failed to generate presigned GET URL for {object_name}"
                ) from e

        return url

    class GeneratePresignedPOSTURLResponseModel(BaseModel):
        url: str
        fields: dict

    async def generate_presigned_POST_URL(
        self,
        object_name: str,
        fields: dict = None,
        conditions: list = None,
        expiration: int = 3600,
    ) -> GeneratePresignedPOSTURLResponseModel:
        """
        Generate a presigned POST URL response to the S3 bucket

        Returns:
          - response: consists of "url" and "fields" for submitting a post request.
        """

        async with self.session.client("s3") as s3:
            try:
                response = await s3.generate_presigned_post(
                    self.s3_bucket_name,
                    object_name,
                    Fields=fields,
                    Conditions=conditions,
                    ExpiresIn=expiration,
                )
            except Exception as e:
                raise Exception(
                    f"Failed to generated presigned POST URL for {object_name}"
                ) from e

        return response
