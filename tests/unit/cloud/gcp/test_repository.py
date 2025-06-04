from unittest.mock import Mock

import pytest
from google.cloud import storage

from cloud_components.cloud.gcp.repository.cloud_storage import CloudStorage
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestCloudStorage:
    """Tests for CloudStorage repository"""

    def setup_method(self):
        self.client = Mock()
        self.logger = Mock()
        self.instance = CloudStorage(connection=self.client, logger=self.logger)

    def test_bucket_getter_without_set(self):
        """Accessing bucket before setting raises AttributeError"""
        with pytest.raises(AttributeError):
            _ = self.instance.bucket

    def test_bucket_setter_assigns_bucket(self):
        """Setting bucket should assign connection.bucket result"""
        bucket = Mock()
        self.client.bucket.return_value = bucket
        self.instance.bucket = "name"
        assert self.instance.bucket is bucket

    def test_save_file_success_and_public(self):
        """save_file should upload data and optionally make object public"""
        bucket = Mock()
        blob = Mock()
        bucket.blob.return_value = blob
        self.instance._bucket = bucket

        result = self.instance.save_file("data", "p", "text/plain", is_public=True)

        assert result is True
        blob.upload_from_string.assert_called_once_with(data="data", content_type="text/plain")
        blob.make_public.assert_called_once_with()

    def test_save_file_error_returns_false(self):
        """save_file should log error and return False on exception"""
        bucket = Mock()
        bucket.blob.side_effect = Exception("err")
        self.instance._bucket = bucket
        assert self.instance.save_file("d", "p", "t") is False
        self.logger.error.assert_called_once()

    def test_get_file_success(self):
        """get_file should return downloaded bytes"""
        bucket = Mock()
        blob = Mock(download_as_bytes=Mock(return_value=b"a"))
        bucket.blob.return_value = blob
        self.instance._bucket = bucket
        assert self.instance.get_file("p") == b"a"

    def test_get_file_error_returns_none(self):
        """get_file should return None when exception raised"""
        bucket = Mock()
        bucket.blob.side_effect = Exception("err")
        self.instance._bucket = bucket
        assert self.instance.get_file("p") is None
        self.logger.error.assert_called_once()

    def test_ls_lists_blobs(self):
        """ls should list blobs using prefix"""
        bucket = Mock()
        bucket.list_blobs.return_value = ["a", "b"]
        self.instance._bucket = bucket
        assert self.instance.ls("p") == ["a", "b"]

    def test_delete_success(self):
        """delete should remove blob and return True"""
        bucket = Mock()
        blob = Mock(generation=1)
        bucket.blob.return_value = blob
        self.instance._bucket = bucket
        assert self.instance.delete("p") is True
        blob.reload.assert_called_once_with()
        blob.delete.assert_called_once_with(if_generation_match=blob.generation)

    def test_delete_error_returns_false(self):
        """delete should return False on exception"""
        bucket = Mock()
        bucket.blob.side_effect = Exception("err")
        self.instance._bucket = bucket
        assert self.instance.delete("p") is False

