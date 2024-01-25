from unittest.mock import Mock, patch

from cloud_components.infra.aws.builder import AwsBuilder


class TestAwsBuilder:
    logger_mock: Mock
    env_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")
        self.env_mock = Mock(name="env")

    @patch("cloud_components.infra.aws.builder.AwsBuilder._set_connection")
    @patch("cloud_components.infra.aws.builder.S3")
    @patch("cloud_components.infra.aws.builder.ResourceConnector")
    def test_build_storage_method__should_call_s3_class(
        self,
        resource_connector: Mock,
        s3: Mock,  # pylint: disable=C0103
        set_connection: Mock,
    ):
        set_connection.return_value = "fake-connection"
        instance = AwsBuilder(
            logger=self.logger_mock,
            access_key="xpto",
            secret_access_key="abcdef",
            env="local",
            localstack_url="http://localhost:4566",
        )
        instance.build_storage()  # pylint: disable=C0103

        set_connection.assert_called_once_with(resource_name="s3")
        s3.assert_called_once_with(
            connection="fake-connection", logger=self.logger_mock
        )
        resource_connector.assert_called_once_with(
            self.logger_mock, "xpto", "abcdef", "local", "http://localhost:4566"
        )

    @patch("cloud_components.infra.aws.builder.AwsBuilder._set_connection")
    @patch("cloud_components.infra.aws.builder.Lambda")
    @patch("cloud_components.infra.aws.builder.ResourceConnector")
    def test_build_function_method__should_call_lambda_class(
        self, resource_connector: Mock, _lambda: Mock, set_connection: Mock
    ):
        set_connection.return_value = "fake-connection"
        instance = AwsBuilder(
            logger=self.logger_mock,
            access_key="xpto",
            secret_access_key="abcdef",
            env="local",
            localstack_url="http://localhost:4566",
        )
        instance.build_function()  # pylint: disable=C0103

        set_connection.assert_called_once_with(resource_name="lambda")
        _lambda.assert_called_once_with(
            connection="fake-connection", logger=self.logger_mock
        )
        resource_connector.assert_called_once_with(
            self.logger_mock, "xpto", "abcdef", "local", "http://localhost:4566"
        )

    @patch("cloud_components.infra.aws.builder.AwsBuilder._set_connection")
    @patch("cloud_components.infra.aws.builder.Sqs")
    @patch("cloud_components.infra.aws.builder.ResourceConnector")
    def test_build_queue_method__should_call_sqs_class(
        self, resource_connector: Mock, sqs: Mock, set_connection: Mock
    ):
        set_connection.return_value = "fake-connection"
        instance = AwsBuilder(
            logger=self.logger_mock,
            access_key="xpto",
            secret_access_key="abcdef",
            env="local",
            localstack_url="http://localhost:4566",
        )
        instance.build_queue()  # pylint: disable=C0103

        set_connection.assert_called_once_with(resource_name="sqs")
        sqs.assert_called_once_with(
            connection="fake-connection", logger=self.logger_mock
        )
        resource_connector.assert_called_once_with(
            self.logger_mock, "xpto", "abcdef", "local", "http://localhost:4566"
        )

    @patch("cloud_components.infra.aws.builder.AwsBuilder._set_connection")
    @patch("cloud_components.infra.aws.builder.Sns")
    @patch("cloud_components.infra.aws.builder.ResourceConnector")
    def test_build_event_method__should_call_sqs_class(
        self, resource_connector: Mock, sns: Mock, set_connection: Mock
    ):
        set_connection.return_value = "fake-connection"
        instance = AwsBuilder(
            logger=self.logger_mock,
            access_key="xpto",
            secret_access_key="abcdef",
            env="local",
            localstack_url="http://localhost:4566",
        )
        instance.build_event()  # pylint: disable=C0103

        set_connection.assert_called_once_with(resource_name="sns")
        sns.assert_called_once_with(
            connection="fake-connection", logger=self.logger_mock
        )
        resource_connector.assert_called_once_with(
            self.logger_mock, "xpto", "abcdef", "local", "http://localhost:4566"
        )
