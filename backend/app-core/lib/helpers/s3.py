import aioboto3
import asyncio
from aiohttp import web
from multidict import MultiDict


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

    async def upload_file(self, local_file_path: str, object_name: str) -> None:
        """
        Upload a file to the S3 bucket
        """

        async with self.session.client("s3") as s3:
            try:
                await s3.upload_file(local_file_path, self.s3_bucket_name, object_name)
            except Exception as e:
                raise Exception(
                    f"Failed to upload the file {local_file_path} to S3 bucket | {str(e)}"
                )

    async def batch_upload_files(self, files: list[tuple[str, str]]) -> None:
        """
        Upload a batch of files to the S3 bucket concurrently
        """

        tasks = []
        for local_path, object_name in files:
            tasks.append(self.upload_file(local_path, object_name))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [r for r in results if isinstance(r, Exception)]
        if exceptions:
            raise Exception(f"Batch upload failed: {exceptions}")

    async def download_file(
        self,
        object_name: str,
        filename: str,
        *,
        request: web.Request,
        chunk_size: int = 69 * 1024,
    ):
        """
        Download a file from the S3 bucket
        """

        async with self.session.client("s3") as s3:
            s3_ob = await s3.get_object(Bucket=self.s3_bucket_name, Key=object_name)

            ob_info = s3_ob["ResponseMetadata"]["HTTPHeaders"]
            resposne = web.StreamResponse(
                headers=MultiDict(
                    {
                        "CONTENT-DISPOSITION": (f"attachment; filename='{filename}'"),
                        "Content-Type": ob_info["content-type"],
                    }
                )
            )
            resposne.content_type = ob_info["content-type"]
            resposne.content_length = ob_info["content-length"]
            await resposne.prepare(request)

            stream = s3_ob["Body"]
            while True:
                chunk = await stream.read(chunk_size)
                if not chunk:
                    break
                await resposne.write(chunk)

        return resposne

    async def generate_presigned_GET_URL(
        self, object_name: str, expiration: int = 3600
    ):
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
                    f"Failed to generate presigned GET URL for {object_name} | {str(e)}"
                )

        return url

    async def generate_presigned_POST_URL(
        self,
        object_name: str,
        fields: dict = None,
        conditions: list = None,
        expiration: int = 3600,
    ):
        """
        Generate a presigned POST URL to the S3 bucket
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
                    f"Failed to generated presigned POST URL for {object_name} | {str(e)}"
                )

        return response
