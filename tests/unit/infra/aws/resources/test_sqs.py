from unittest.mock import Mock
from botocore.exceptions import ClientError

import pytest

from cloud_components.infra.aws.resources.sqs import Sqs


class TestSqs:
    connection_mock: Mock
    logger_mock: Mock

    def setup_method(self):
        self.connection_mock = Mock(name="connection")
        self.logger_mock = Mock(name="logger")

    def test_queue_property__should_queue_have_a_none_value__expected_error(  # pylint: disable=C0301
        self,
    ):
        queue = None
        sqs = Sqs(connection=self.connection_mock, logger=self.logger_mock)

        with pytest.raises(ValueError) as err:
            queue = sqs.queue
        assert str(err.value) == "Queue not found"
        assert not queue

    def test_queue_property__should_get_a_value__expected_mock_value(  # pylint: disable=C0301
        self,
    ):
        queue = Mock(name="queue")
        sqs = Sqs(connection=self.connection_mock, logger=self.logger_mock)
        sqs._queue = queue  # pylint: disable=W0212

        queue_from_instance = sqs.queue

        assert queue_from_instance
        assert isinstance(queue_from_instance, Mock)
        assert queue_from_instance == queue

    def test_queue_property__should_set_an_value__expected_get_queue_by_name_call_from_connection_object(  # pylint: disable=C0301
        self,
    ):
        sqs = Sqs(connection=self.connection_mock, logger=self.logger_mock)
        sqs.queue = "test-queue"

        self.connection_mock.get_queue_by_name.assert_called_once_with(
            QueueName="test-queue"
        )

    def test_send_message_method__should_send_a_message__expected_send_message_call_from_queue_property(  # pylint: disable=C0301
        self,
    ):
        queue = Mock(name="queue")
        sqs = Sqs(connection=self.connection_mock, logger=self.logger_mock)
        sqs._queue = queue  # pylint: disable=W0212

        sended_message = sqs.send_message(message="blablabla")

        queue.send_message.assert_called_once_with(MessageBody="blablabla")
        assert isinstance(sended_message, bool)
        assert sended_message

    def test_send_message__should_not_send_a_message__expected_error(  # pylint: disable=C0301
        self,
    ):
        queue = Mock(name="queue")
        sqs = Sqs(connection=self.connection_mock, logger=self.logger_mock)
        sqs._queue = queue  # pylint: disable=W0212
        queue.send_message.side_effect = ClientError(
            error_response={"Error": {"Code": 400, "Message": "test error"}},
            operation_name="not-found-error",
        )

        sended_message = sqs.send_message(message="blablabla")

        assert isinstance(sended_message, bool)
        assert not sended_message
        queue.send_message.assert_called_once_with(MessageBody="blablabla")
