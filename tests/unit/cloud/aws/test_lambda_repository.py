from unittest.mock import Mock
from botocore.exceptions import ClientError

from cloud_components.cloud.aws.repository.lambda_function import Lambda


class TestLambda:
    def setup_method(self):
        self.connection = Mock(name="connection")
        self.logger = Mock(name="logger")
        self.instance = Lambda(connection=self.connection, logger=self.logger)
        self.instance.function = "my-function"

    def test_execute_should_invoke_and_return_payload(self):
        payload = b"{}"
        stream = Mock(name="payload")
        stream.read.return_value = b"result"
        self.connection.invoke.return_value = {"Payload": stream}

        result = self.instance.execute(payload)

        assert result == b"result"
        self.connection.invoke.assert_called_once_with(
            FunctionName="my-function", Payload=payload
        )

    def test_execute_when_error_should_log_and_return_none(self):
        self.connection.invoke.side_effect = ClientError({"Error": {}}, "invoke")

        result = self.instance.execute(b"{}")

        assert result is None
        self.logger.error.assert_called_once()
