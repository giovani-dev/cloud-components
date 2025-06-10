# pylint: disable=attribute-defined-outside-init, protected-access
from unittest.mock import Mock
from botocore.exceptions import ClientError

from cloud_components.cloud.aws.repository.sqs import Sqs


class TestSqs:
    def setup_method(self):
        self.connection = Mock(name="connection")
        self.logger = Mock(name="logger")
        self.instance = Sqs(connection=self.connection, logger=self.logger)
        self.connection.get_queue_by_name.return_value = Mock(name="queue")
        self.instance.queue = "queue"
        self.queue = self.connection.get_queue_by_name.return_value

    def test_receive_message_should_return_body_and_delete(self):
        message = Mock(name="message")
        message.body = "hello"
        self.queue.receive_messages.return_value = [message]

        result = self.instance.receive_message()

        assert result == "hello"
        self.queue.receive_messages.assert_called_once_with(MaxNumberOfMessages=1)
        message.delete.assert_called_once_with()

    def test_receive_message_when_empty_should_return_empty_string(self):
        self.queue.receive_messages.return_value = []

        result = self.instance.receive_message()

        assert result == ""

    def test_receive_message_when_error_should_log_and_return_empty_string(self):
        self.queue.receive_messages.side_effect = ClientError({"Error": {}}, "receive")

        result = self.instance.receive_message()

        assert result == ""
        self.logger.error.assert_called_once()
