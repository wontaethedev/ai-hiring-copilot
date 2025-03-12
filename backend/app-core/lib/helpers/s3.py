from pydantic import BaseModel
import aioboto3
import asyncio
import io

from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from lib.helpers.ulid import generate_ulid


class UploadFileResult(BaseModel):
    file: UploadFile
    s3_object_key: str


class UploadResult(BaseModel):
    s3_object_key: str | None
    file: UploadFile  # The original file object
    success: bool


class GeneratePresignedPOSTURLResponseModel(BaseModel):
    url: str
    fields: dict


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
            raise Exception("Failed to create AWS S3 session") from e

    async def upload_file(
        self,
        organization_id: str,
        file: UploadFile,
    ) -> UploadFileResult:
        """
        Upload a file to the S3 bucket
        """

        ulid = generate_ulid()

        s3_object_key = f"resume/{organization_id}/{ulid}"

        async with self.session.client("s3") as s3:
            try:
                await s3.upload_fileobj(file.file, self.s3_bucket_name, s3_object_key)
            except Exception as e:
                raise Exception(
                    f"Failed to upload the file {file.filename} to S3 bucket"
                ) from e

        return UploadFileResult(file=file, s3_object_key=s3_object_key)

    async def batch_upload_files(
        self,
        organization_id: str,
        files: list[UploadFile],
    ) -> list[UploadResult]:
        """
        Upload a batch of files to the S3 bucket concurrently

        Returns:
          - upload_results: A list of UploadResult showing the result of batch upload
        """

        tasks = [
            self.upload_file(organization_id=organization_id, file=file)
            for file in files
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        upload_results = []
        for file, result in zip(files, results):
            if isinstance(result, Exception):
                upload_results.append(
                    UploadResult(s3_object_key=None, file=file, success=False)
                )
            elif isinstance(result, UploadFileResult):
                upload_results.append(
                    UploadResult(
                        s3_object_key=result.s3_object_key,
                        file=file,
                        success=True,
                    )
                )
            else:
                raise Exception(
                    "Unexpected error occurred while returning batch upload results"
                )

        return upload_results

    async def download_file(self, s3_object_key: str) -> io.BytesIO:
        async with self.session.client("s3") as s3:
            try:
                bytes_io = io.BytesIO()
                await s3.download_fileobj(
                    Bucket=self.s3_bucket_name, Key=s3_object_key, Fileobj=bytes_io
                )
                bytes_io.seek(0)
            except Exception as e:
                raise Exception("Failed to download a file from S3 bucket") from e

        return bytes_io

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

    async def generate_presigned_POST_URL(
        self,
        object_name: str,
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
                    ExpiresIn=expiration,
                )
            except Exception as e:
                raise Exception(
                    f"Failed to generated presigned POST URL for {object_name}"
                ) from e

            url = response.get("url")
            fields = response.get("fields")
            if url is None or fields is None:
                raise Exception(
                    "S3 generate presigned post does not contain all expected fields"
                )

        return GeneratePresignedPOSTURLResponseModel(url=url, fields=fields)
