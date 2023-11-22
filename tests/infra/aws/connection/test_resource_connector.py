from unittest.mock import Mock, patch

from cloud_components.infra.aws.connection.resource_connector import ResourceConnector


class TestResourceConnector:
    logger_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")

    @patch("cloud_components.infra.aws.connection.resource_connector.ConnectorFactory")
    def test_connect_method__should_connect_in_local_enviroment_with_localstack(
        self, connection_factory: Mock
    ):
        manufactured_connection = Mock(name="manufactured_connection")
        connection_factory.manufacture.return_value = manufactured_connection

        resource_connector = ResourceConnector(
            logger=self.logger_mock,
            access_key="abc",
            secret_access_key="mnop",
            env="local",
            localstack_url="http://localhost:3000",
        )
        connection = resource_connector.connect("dynamodb")

        assert connection == manufactured_connection
        connection_factory.manufacture.assert_called_once_with(
            resource="dynamodb",
            aws_access_key_id="abc",
            aws_secret_access_key="mnop",
            endpoint_url="http://localhost:3000",
        )

    @patch("cloud_components.infra.aws.connection.resource_connector.ConnectorFactory")
    def test_connect_method__should_connect_in_local_enviroment_with_aws_cloud(
        self, connection_factory: Mock
    ):
        manufactured_connection = Mock(name="manufactured_connection")
        connection_factory.manufacture.return_value = manufactured_connection

        resource_connector = ResourceConnector(
            logger=self.logger_mock,
            access_key="abc",
            secret_access_key="mnop",
            env="local",
        )
        connection = resource_connector.connect("dynamodb")

        assert connection == manufactured_connection
        connection_factory.manufacture.assert_called_once_with(
            resource="dynamodb",
            aws_access_key_id="abc",
            aws_secret_access_key="mnop",
        )

    @patch("cloud_components.infra.aws.connection.resource_connector.ConnectorFactory")
    def test_connect_method__shoud_connect_in_aws_cloud(self, connection_factory: Mock):
        manufactured_connection = Mock(name="manufactured_connection")
        connection_factory.manufacture.return_value = manufactured_connection

        resource_connector = ResourceConnector(
            logger=self.logger_mock,
            access_key="abc",
            secret_access_key="mnop",
        )
        connection = resource_connector.connect("dynamodb")

        assert connection == manufactured_connection
        connection_factory.manufacture.assert_called_once_with(resource="dynamodb")
