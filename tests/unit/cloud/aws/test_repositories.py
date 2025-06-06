import pytest
from unittest.mock import Mock

from botocore.exceptions import ClientError

from cloud_components.cloud.aws.repository.sns import Sns
from cloud_components.cloud.aws.repository.lambda_function import Lambda
from cloud_components.cloud.aws.repository.sqs import Sqs
from cloud_components.cloud.aws.repository.s3 import S3
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestSns:
    """Tests for the SNS repository"""

    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.instance = Sns(connection=self.connection, logger=self.logger)

    def test_source_property_without_set_raises(self):
        """Accessing source before setting should raise ResourceNameNotFound"""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.source

    def test_send_success(self):
        """send() should publish message and return True"""
        self.instance.source = "arn"
        result = self.instance.send({"x": 1})
        assert result is True
        self.connection.publish.assert_called_once()

    def test_send_error_logs_and_returns_false(self):
        """send() should log error when boto raises ClientError"""
        self.instance.source = "arn"
        self.connection.publish.side_effect = ClientError({}, "publish")
        result = self.instance.send({})
        assert result is False
        self.logger.error.assert_called_once()


class TestLambda:
    """Tests for Lambda repository"""

    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.instance = Lambda(connection=self.connection, logger=self.logger)

    def test_function_property_without_set(self):
        """Accessing function before setting should raise ResourceNameNotFound"""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.function

    def test_function_property_set_and_get(self):
        """After setting function, getter should return the same value"""
        self.instance.function = "my-func"
        assert self.instance.function == "my-func"


class TestSqs:
    """Tests for Sqs repository"""

    def setup_method(self):
        self.resource = Mock()
        self.logger = Mock()
        self.instance = Sqs(connection=self.resource, logger=self.logger)

    def test_queue_getter_without_set(self):
        """Getting queue before assigning should raise ResourceNameNotFound"""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.queue

    def test_queue_setter_fetches_queue(self):
        """Setting queue should fetch queue by name"""
        queue = Mock()
        self.resource.get_queue_by_name.return_value = queue
        self.instance.queue = "name"
        assert self.instance.queue is queue

    def test_send_message_success(self):
        """send_message should call queue.send_message and return True"""
        queue = Mock()
        self.instance._queue = queue
        result = self.instance.send_message("hello")
        assert result is True
        queue.send_message.assert_called_once_with(MessageBody="hello")

    def test_send_message_error(self):
        """send_message should log error and return False on exception"""
        queue = Mock()
        queue.send_message.side_effect = ClientError({}, "send_message")
        self.instance._queue = queue
        result = self.instance.send_message("msg")
        assert result is False
        self.logger.error.assert_called_once()


class TestS3:
    """Tests for S3 repository"""

    def setup_method(self):
        self.resource = Mock()
        self.logger = Mock()
        self.instance = S3(connection=self.resource, logger=self.logger)

    def test_bucket_property_without_set(self):
        """Accessing bucket before setting should raise ResourceNameNotFound"""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.bucket

    def test_save_file_public(self):
        """save_file should put object with public-read ACL when is_public"""
        bucket = Mock()
        self.instance._bucket = bucket
        result = self.instance.save_file(b"data", "f.txt", "text/plain", is_public=True)
        assert result is True
        bucket.put_object.assert_called_once()

    def test_save_file_error(self):
        """save_file should log and return False on ClientError"""
        bucket = Mock()
        bucket.put_object.side_effect = ClientError({}, "put_object")
        self.instance._bucket = bucket
        result = self.instance.save_file(b"", "f", "text/plain")
        assert result is False
        self.logger.error.assert_called_once()

    def test_get_file_success(self):
        """get_file should download bytes when available"""
        obj = Mock()
        obj.get.return_value = {"Body": Mock(read=Mock(return_value=b"abc"))}
        bucket = Mock()
        bucket.Object.return_value = obj
        self.instance._bucket = bucket
        assert self.instance.get_file("f") == b"abc"

    def test_get_file_error(self):
        """get_file should return None on exception"""
        bucket = Mock()
        bucket.Object.side_effect = ClientError({}, "get")
        self.instance._bucket = bucket
        assert self.instance.get_file("f") is None
        self.logger.error.assert_called_once()

    def test_ls_lists_objects(self):
        """ls should list object keys for prefix"""
        bucket = Mock()
        bucket.objects.filter.return_value = [Mock(key="a"), Mock(key="b")]
        self.instance._bucket = bucket
        assert self.instance.ls("p") == ["a", "b"]

    def test_delete_success(self):
        """delete should remove object and return True"""
        bucket = Mock()
        self.instance._bucket = bucket
        assert self.instance.delete("path") is True
        bucket.Object.assert_called_once_with("path")

    def test_delete_failure(self):
        """delete should return False when exception raised"""
        bucket = Mock()
        bucket.Object.side_effect = Exception("err")
        self.instance._bucket = bucket
        assert self.instance.delete("path") is False

