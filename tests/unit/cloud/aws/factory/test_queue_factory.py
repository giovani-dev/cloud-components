from unittest.mock import Mock, patch

from cloud_components.cloud.aws.factory.queue_factory import QueueFactory


@patch('cloud_components.cloud.aws.factory.queue_factory.boto3')
class TestQueueFactory:
    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.env.get.side_effect = ['key', 'secret', 'endpoint']

    def test_manufacture_builds_sqs(self, boto3_mock: Mock):
        """Factory should create an SQS repository with boto3."""
        resource = boto3_mock.resource.return_value
        factory = QueueFactory(logger=self.logger, env=self.env)
        sqs = factory.manufacture()
        assert sqs.connection is resource
        boto3_mock.resource.assert_called_once_with(
            'sqs',
            aws_access_key_id='key',
            aws_secret_access_key='secret',
            endpoint_url='endpoint',
        )
