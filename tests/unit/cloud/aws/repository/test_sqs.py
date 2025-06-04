import pytest
from unittest.mock import Mock

from botocore.exceptions import ClientError
from cloud_components.cloud.aws.repository.sqs import Sqs
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestSqs:
    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.queue = Mock()
        self.connection.get_queue_by_name.return_value = self.queue
        self.instance = Sqs(connection=self.connection, logger=self.logger)

    def test_queue_property_without_set(self):
        """Accessing ``queue`` before setting should raise an error."""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.queue

    def test_queue_setter(self):
        """Setting queue name should retrieve the boto3 queue object."""
        self.instance.queue = "q"
        assert self.instance.queue == self.queue
        self.connection.get_queue_by_name.assert_called_once_with(QueueName="q")

    def test_send_message_success(self):
        """send_message should publish a message to the queue."""
        self.instance.queue = "q"
        assert self.instance.send_message("hello")
        self.queue.send_message.assert_called_once_with(MessageBody="hello")

    def test_send_message_failure_returns_false(self):
        """send_message should return ``False`` and log when errors occur."""
        self.instance.queue = "q"
        self.queue.send_message.side_effect = ClientError({}, "send_message")
        assert not self.instance.send_message("hello")
        self.logger.error.assert_called_once()
