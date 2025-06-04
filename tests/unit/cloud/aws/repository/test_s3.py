import pytest
from unittest.mock import Mock

from botocore.exceptions import ClientError
from cloud_components.cloud.aws.repository.s3 import S3
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestS3:
    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.bucket = Mock()
        self.connection.Bucket.return_value = self.bucket
        self.instance = S3(connection=self.connection, logger=self.logger)

    def test_bucket_property_without_set(self):
        """Accessing ``bucket`` before setting it should raise an error."""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.bucket

    def test_bucket_setter_creates_bucket_obj(self):
        """Setting a bucket name should instantiate a Bucket object."""
        self.instance.bucket = "mybucket"
        assert self.instance.bucket == self.bucket
        self.connection.Bucket.assert_called_once_with("mybucket")

    def test_save_file_success_public(self):
        """save_file should upload data and make it public when requested."""
        self.instance.bucket = "b"
        assert self.instance.save_file(b"data", "path", "text/plain", True)
        self.bucket.put_object.assert_called_once_with(
            Key="path", Body=b"data", ACL="public-read", ContentType="text/plain"
        )

    def test_save_file_failure_logs_error(self):
        """save_file should log and return False if boto3 raises errors."""
        self.instance.bucket = "b"
        self.bucket.put_object.side_effect = ClientError({}, "put_object")
        assert not self.instance.save_file(b"d", "p", "t")
        self.logger.error.assert_called_once()

    def test_get_file_success(self):
        """get_file should read bytes from the object."""
        self.instance.bucket = "b"
        obj = self.bucket.Object.return_value
        obj.get.return_value = {"Body": Mock(read=Mock(return_value=b"content"))}
        assert self.instance.get_file("file") == b"content"

    def test_get_file_failure_returns_none(self):
        """On error retrieving a file, ``None`` should be returned."""
        self.instance.bucket = "b"
        obj = self.bucket.Object.return_value
        obj.get.side_effect = ClientError({}, "get_object")
        assert self.instance.get_file("file") is None
        self.logger.error.assert_called()

    def test_ls_returns_keys(self):
        """ls should return a list of object keys for the prefix."""
        self.instance.bucket = "b"
        self.bucket.objects.filter.return_value = [Mock(key="a"), Mock(key="b")]
        assert self.instance.ls("prefix") == ["a", "b"]

    def test_delete_success(self):
        """delete should remove the object and return ``True``."""
        self.instance.bucket = "b"
        assert self.instance.delete("f")
        self.bucket.Object.assert_called_once_with("f")
        self.bucket.Object.return_value.delete.assert_called_once_with()

    def test_delete_failure_returns_false(self):
        """delete should log errors and return ``False`` on failure."""
        self.instance.bucket = "b"
        self.bucket.Object.return_value.delete.side_effect = Exception()
        assert not self.instance.delete("f")
