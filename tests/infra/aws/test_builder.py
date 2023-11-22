from unittest.mock import Mock, patch

from cloud_components.infra.aws.builder import AwsBuilder


class TestAwsBuilder:
    logger_mock: Mock
    env_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")
        self.env_mock = Mock(name="env")

    @patch("cloud_components.infra.aws.builder.S3")
    @patch("cloud_components.infra.aws.builder.ResourceConnector")
    def test_build_storage__call_s3_class__expected_call_with_mock_params(
        self, resource_connector_mock: Mock, s3_mock: Mock
    ):
        methods_mock = Mock(name="resource_connector_methods")
        methods_mock.connect.return_value = "connection"
        resource_connector_mock.return_value = methods_mock

        s3_mock.return_value = "s3 call return"

        instance = AwsBuilder(
            logger=self.logger_mock,
            access_key="xpto",
            secret_access_key="abcdef",
            env="local",
            localstack_url="http://localhost:4566",
        )
        s3 = instance.build_storage()  # pylint: disable=C0103

        resource_connector_mock.assert_called_once_with(
            self.logger_mock,
            "xpto",
            "abcdef",
            "local",
            "http://localhost:4566",
        )
        s3_mock.assert_called_once_with(
            connection="connection", logger=self.logger_mock
        )
        assert s3 == "s3 call return"
