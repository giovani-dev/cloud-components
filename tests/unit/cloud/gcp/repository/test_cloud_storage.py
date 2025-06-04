import pytest
from unittest.mock import Mock

from cloud_components.cloud.gcp.repository.cloud_storage import CloudStorage
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestCloudStorage:
    def setup_method(self):
        self.client = Mock()
        self.logger = Mock()
        self.bucket = Mock()
        self.client.bucket.return_value = self.bucket
        self.instance = CloudStorage(connection=self.client, logger=self.logger)

    def test_bucket_property_without_set(self):
        """Accessing ``bucket`` before setting should raise an error."""
        with pytest.raises(AttributeError):
            _ = self.instance.bucket

    def test_bucket_setter(self):
        """Setting bucket name should fetch a bucket client."""
        self.instance.bucket = "b"
        assert self.instance.bucket == self.bucket
        self.client.bucket.assert_called_once_with("b")

    def test_save_file_success_public(self):
        """save_file should upload and make blob public when requested."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        assert self.instance.save_file("data", "p", "t", True)
        blob.upload_from_string.assert_called_once_with(data="data", content_type="t")
        blob.make_public.assert_called_once_with()

    def test_save_file_failure_returns_false(self):
        """save_file should return ``False`` when upload fails."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        blob.upload_from_string.side_effect = Exception()
        assert not self.instance.save_file("d", "p", "t")
        self.logger.error.assert_called_once()

    def test_get_file_success(self):
        """get_file should retrieve bytes from storage."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        blob.download_as_bytes.return_value = b"c"
        assert self.instance.get_file("p") == b"c"

    def test_get_file_failure_returns_none(self):
        """Return ``None`` and log when download fails."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        blob.download_as_bytes.side_effect = Exception()
        assert self.instance.get_file("p") is None
        self.logger.error.assert_called_once()

    def test_ls_returns_list(self):
        """ls should list blobs in the bucket for a prefix."""
        self.instance.bucket = "b"
        self.bucket.list_blobs.return_value = [1, 2]
        assert self.instance.ls("p") == [1, 2]

    def test_delete_success(self):
        """delete should remove the blob from the bucket."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        assert self.instance.delete("p")
        blob.reload.assert_called_once_with()
        blob.delete.assert_called_once()

    def test_delete_failure_returns_false(self):
        """delete should return ``False`` when deletion fails."""
        self.instance.bucket = "b"
        blob = self.bucket.blob.return_value
        blob.reload.side_effect = Exception()
        assert not self.instance.delete("p")
