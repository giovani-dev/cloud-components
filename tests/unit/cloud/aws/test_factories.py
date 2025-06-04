from unittest.mock import Mock, patch

from cloud_components.cloud.aws.factory.event_factory import Eventfactory
from cloud_components.cloud.aws.factory.function_factory import FunctionFactory
from cloud_components.cloud.aws.factory.queue_factory import QueueFactory
from cloud_components.cloud.aws.factory.storage_factory import StorageFactory


class TestEventFactory:
    """Eventfactory.manufacture"""

    def test_manufacture_creates_sns_with_client(self):
        logger = Mock()
        env = Mock()
        env.get.side_effect = ["key", "secret", "endpoint"]
        connection = Mock(name="sns_client")
        with patch("boto3.client", return_value=connection) as boto:
            result = Eventfactory(logger, env).manufacture()
            assert result.connection is connection
            boto.assert_called_once_with(
                "sns",
                aws_access_key_id="key",
                aws_secret_access_key="secret",
                endpoint_url="endpoint",
            )

class TestFunctionFactory:
    """FunctionFactory.manufacture"""

    def test_manufacture_creates_lambda_client(self):
        logger = Mock()
        env = Mock()
        env.get.side_effect = ["key", "secret", "endpoint"]
        connection = Mock(name="lambda_client")
        with patch("boto3.client", return_value=connection) as boto:
            result = FunctionFactory(logger, env).manufacture()
            assert result.connection is connection
            boto.assert_called_once_with(
                "lambda",
                aws_access_key_id="key",
                aws_secret_access_key="secret",
                endpoint_url="endpoint",
            )


class TestQueueFactory:
    """QueueFactory.manufacture"""

    def test_manufacture_creates_sqs_resource(self):
        logger = Mock()
        env = Mock()
        env.get.side_effect = ["key", "secret", "endpoint"]
        resource = Mock(name="sqs_resource")
        with patch("boto3.resource", return_value=resource) as boto:
            result = QueueFactory(logger, env).manufacture()
            assert result.connection is resource
            boto.assert_called_once_with(
                "sqs",
                aws_access_key_id="key",
                aws_secret_access_key="secret",
                endpoint_url="endpoint",
            )


class TestStorageFactory:
    """StorageFactory.manufacture"""

    def test_manufacture_creates_s3_resource(self):
        logger = Mock()
        env = Mock()
        env.get.side_effect = ["key", "secret", "endpoint"]
        resource = Mock(name="s3_resource")
        with patch("boto3.resource", return_value=resource) as boto:
            result = StorageFactory(logger, env).manufacture()
            assert result.connection is resource
            boto.assert_called_once_with(
                "s3",
                aws_access_key_id="key",
                aws_secret_access_key="secret",
                endpoint_url="endpoint",
            )

