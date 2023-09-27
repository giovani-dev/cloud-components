from unittest.mock import patch, Mock

from cloud_components.infra.aws.connection.connector_factory import ConnectorFactory


class TestAwsConnectorFactory:
    @patch("cloud_components.infra.aws.connection.connector_factory.boto3")
    def test_manufacture__service_as_a_lambda__expected_client_frunction_call_from_boto3(
        self, boto3_mock: Mock
    ):
        boto3_mock.client.return_value = "client"
        callback = ConnectorFactory.manufacture(
            resource="lambda", endpoint_url="http://localstack:5365"
        )

        assert callback == "client"
        boto3_mock.client.assert_called_once_with(
            "lambda", endpoint_url="http://localstack:5365"
        )

    @patch("cloud_components.infra.aws.connection.connector_factory.boto3")
    def test_manufacture__service_as_a_s3__expected_resource_frunction_call_from_boto3(
        self, boto3_mock: Mock
    ):
        boto3_mock.resource.return_value = "resource"
        callback = ConnectorFactory.manufacture(
            resource="s3", endpoint_url="http://localstack:5365"
        )

        assert callback == "resource"
        boto3_mock.resource.assert_called_once_with(
            "s3", endpoint_url="http://localstack:5365"
        )
