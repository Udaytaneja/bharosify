import abc
import os
from pathlib import Path

from backend.app.core.config import settings

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class BaseStorageService(abc.ABC):
    @abc.abstractmethod
    async def save_file(
        self, file_bytes: bytes, stored_filename: str, content_type: str
    ) -> str:
        """Saves file bytes and returns the stored object key / file path."""
        pass

    @abc.abstractmethod
    async def get_file(self, stored_filename: str) -> tuple[bytes, str]:
        """Retrieves stored file bytes and content_type."""
        pass


class LocalStorageService(BaseStorageService):
    async def save_file(
        self, file_bytes: bytes, stored_filename: str, content_type: str
    ) -> str:
        file_path = UPLOAD_DIR / stored_filename
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        return str(file_path)

    async def get_file(self, stored_filename: str) -> tuple[bytes, str]:
        file_path = UPLOAD_DIR / stored_filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{stored_filename}' not found in local storage.")
        with open(file_path, "rb") as f:
            content = f.read()
        return content, "application/pdf"


class S3StorageService(BaseStorageService):
    """Production S3 / Cloudflare R2 object storage provider."""

    def __init__(self):
        self.bucket = settings.s3_bucket_name
        self.endpoint_url = settings.s3_endpoint_url or None
        self.aws_access_key = settings.s3_access_key_id
        self.aws_secret_key = settings.s3_secret_access_key
        self.region = settings.s3_region

    def _get_client(self):
        import boto3

        kwargs = {"region_name": self.region}
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url
        if self.aws_access_key and self.aws_secret_key:
            kwargs["aws_access_key_id"] = self.aws_access_key
            kwargs["aws_secret_access_key"] = self.aws_secret_key

        return boto3.client("s3", **kwargs)

    async def save_file(
        self, file_bytes: bytes, stored_filename: str, content_type: str
    ) -> str:
        if not self.bucket:
            # Fallback to local storage if S3_BUCKET_NAME is not configured
            local_service = LocalStorageService()
            return await local_service.save_file(file_bytes, stored_filename, content_type)

        client = self._get_client()
        client.put_object(
            Bucket=self.bucket,
            Key=stored_filename,
            Body=file_bytes,
            ContentType=content_type,
        )
        return f"s3://{self.bucket}/{stored_filename}"

    async def get_file(self, stored_filename: str) -> tuple[bytes, str]:
        if not self.bucket:
            local_service = LocalStorageService()
            return await local_service.get_file(stored_filename)

        client = self._get_client()
        res = client.get_object(Bucket=self.bucket, Key=stored_filename)
        content = res["Body"].read()
        content_type = res.get("ContentType", "application/pdf")
        return content, content_type


def get_storage_service() -> BaseStorageService:
    if settings.storage_provider.lower() in {"s3", "r2", "object_storage"}:
        return S3StorageService()
    return LocalStorageService()


storage_service = get_storage_service()
