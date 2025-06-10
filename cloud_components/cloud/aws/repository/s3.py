from typing import Any, Union
from botocore.exceptions import ClientError

from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.logger import ILogger


class S3(IStorage):
    """Implementation of :class:`IStorage` for Amazon S3."""

    _bucket = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        """Create a new S3 repository with an existing boto3 connection."""
        self.connection = connection
        self.logger = logger

    @property
    def bucket(self) -> Any:
        """Return the configured S3 bucket."""
        if not self._bucket:
            raise ResourceNameNotFound("Storage not found, please provide a name to it")
        return self._bucket

    @bucket.setter
    def bucket(self, name: str) -> None:
        """Set the current bucket by ``name``."""
        self._bucket = self.connection.Bucket(name)

    def save_file(
        self,
        data: bytes,
        file_path: str,
        content_type: str,
        is_public: bool = False,
    ) -> bool:
        """Save ``data`` to ``file_path`` in the configured bucket."""
        try:
            if is_public:
                self.bucket.put_object(
                    Key=file_path,
                    Body=data,
                    ACL="public-read",
                    ContentType=content_type,
                )
            else:
                self.bucket.put_object(
                    Key=file_path, Body=data, ContentType=content_type
                )
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to save a file in S3. Error detail: {err}"
            )
            return False
        return True

    def get_file(self, file_path: str) -> Union[bytes, None]:
        """Retrieve a file from the bucket and return its contents."""
        try:
            content = self.bucket.Object(file_path)
            content = content.get()["Body"].read()
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to get a file in S3. Error detail: {err}"
            )
            return None
        return content

    def ls(self, path: str) -> list[str]:  # pylint: disable=C0103
        """List keys under ``path`` in the bucket."""
        return [_object.key for _object in self.bucket.objects.filter(Prefix=path)]

    def delete(self, file_path: str) -> bool:
        """Delete ``file_path`` from the bucket."""
        try:
            self.bucket.Object(file_path).delete()
        except Exception as err:  # pylint: disable=W0612,W0718
            return False
        return True
