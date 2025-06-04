from unittest.mock import Mock, patch

from cloud_components.cloud.aws.factory.event_factory import Eventfactory


@patch('cloud_components.cloud.aws.factory.event_factory.boto3')
class TestEventFactory:
    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.env.get.side_effect = ['key', 'secret', 'endpoint']

    def test_manufacture_builds_sns(self, boto3_mock: Mock):
        """Factory should create an SNS repository using boto3."""
        client = boto3_mock.client.return_value
        instance = Eventfactory(logger=self.logger, env=self.env)
        sns = instance.manufacture()
        assert sns.connection is client
        boto3_mock.client.assert_called_once_with(
            'sns',
            aws_access_key_id='key',
            aws_secret_access_key='secret',
            endpoint_url='endpoint',
        )
