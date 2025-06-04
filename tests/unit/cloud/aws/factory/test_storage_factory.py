from unittest.mock import Mock, patch

from cloud_components.cloud.aws.factory.storage_factory import StorageFactory


@patch('cloud_components.cloud.aws.factory.storage_factory.boto3')
class TestStorageFactory:
    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.env.get.side_effect = ['key', 'secret', 'endpoint']

    def test_manufacture_builds_s3(self, boto3_mock: Mock):
        """Factory should create an S3 repository using boto3."""
        resource = boto3_mock.resource.return_value
        factory = StorageFactory(logger=self.logger, env=self.env)
        s3 = factory.manufacture()
        assert s3.connection is resource
        boto3_mock.resource.assert_called_once_with(
            's3',
            aws_access_key_id='key',
            aws_secret_access_key='secret',
            endpoint_url='endpoint',
        )
