from unittest.mock import Mock, patch

from cloud_components.cloud.aws.factory.function_factory import FunctionFactory


@patch('cloud_components.cloud.aws.factory.function_factory.boto3')
class TestFunctionFactory:
    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.env.get.side_effect = ['key', 'secret', 'endpoint']

    def test_manufacture_builds_lambda(self, boto3_mock: Mock):
        """Factory should build a Lambda repository using boto3."""
        client = boto3_mock.client.return_value
        factory = FunctionFactory(logger=self.logger, env=self.env)
        lmb = factory.manufacture()
        assert lmb.connection is client
        boto3_mock.client.assert_called_once_with(
            'lambda',
            aws_access_key_id='key',
            aws_secret_access_key='secret',
            endpoint_url='endpoint',
        )
