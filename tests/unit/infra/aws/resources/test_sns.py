from unittest.mock import Mock, call, patch
from botocore.exceptions import ClientError

import pytest

from cloud_components.infra.aws.resources.sns import Sns


class TestSns:
    connection_mock: Mock
    logger_mock: Mock

    def setup_method(self):
        self.connection_mock = Mock(name="connection")
        self.logger_mock = Mock(name="logger")

    def test_source_method__should_source_have_a_none_value__expected_error(self):
        source = None
        sns = Sns(connection=self.connection_mock, logger=self.logger_mock)

        with pytest.raises(ValueError) as err:
            source = sns.source
        assert str(err.value) == "Source not found"
        assert not source

    def test_source_method__shoud_source_have_a_value__expected_vlaue_return(self):
        sns = Sns(connection=self.connection_mock, logger=self.logger_mock)
        sns.source = "any value"

        assert sns.source == "any value"

    @patch("cloud_components.infra.aws.resources.sns.json")
    def test_send_method__shoud_send_structured_message__expected_published_message(
        self, json: Mock
    ):
        source = Mock(name="source")
        json.dumps.side_effect = [
            '{"test": "123 testing 123"}',
            '{"default": "{\\"test\\": \\"123 testing 123\\"}"}',
        ]
        sns = Sns(connection=self.connection_mock, logger=self.logger_mock)
        sns._source = source

        is_sended = sns.send(
            message={"test": "123 testing 123"}, message_structere="json"
        )

        assert isinstance(is_sended, bool)
        assert is_sended
        json.dumps.assert_has_calls(
            [
                call({"test": "123 testing 123"}),
                call({"default": '{"test": "123 testing 123"}'}),
            ]
        )
        self.connection_mock.publish.assert_called_once_with(
            TargetArn=source,
            Message='{"default": "{\\"test\\": \\"123 testing 123\\"}"}',
            MessageStructure="json",
        )

    @patch("cloud_components.infra.aws.resources.sns.json")
    def test_send_method__should_send_message__expected_published_message(
        self, json: Mock
    ):
        source = Mock(name="source")
        sns = Sns(connection=self.connection_mock, logger=self.logger_mock)
        sns._source = source
        json.dumps.return_value = '{"test": "123 testing 123"}'

        is_sended = sns.send(message={"test": "123 testing 123"})

        assert isinstance(is_sended, bool)
        assert is_sended
        json.dumps.assert_called_once_with({"test": "123 testing 123"})
        self.connection_mock.publish.assert_called_once_with(
            TargetArn=source, Message='{"test": "123 testing 123"}'
        )

    @patch("cloud_components.infra.aws.resources.sns.json")
    def test_send_method__should_an_error_occurred_when_send_message__expected_client_error_capture(
        self, json: Mock
    ):
        source = Mock(name="source")
        sns = Sns(connection=self.connection_mock, logger=self.logger_mock)
        sns._source = source
        json.dumps.return_value = '{"test": "123 testing 123"}'
        self.connection_mock.publish.side_effect = ClientError(
            error_response={"Error": {"Code": 400, "Message": "test error"}},
            operation_name="not-found-error",
        )

        is_sended = sns.send(message={"test": "123 testing 123"})

        assert isinstance(is_sended, bool)
        assert not is_sended
        json.dumps.assert_called_once_with({"test": "123 testing 123"})
        self.connection_mock.publish.assert_called_once_with(
            TargetArn=source, Message='{"test": "123 testing 123"}'
        )
