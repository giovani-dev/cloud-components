from unittest.mock import Mock, patch

from cloud_components.infra.factory import InfraFactory


class TestInfraFactory:
    logger_mock: Mock
    env_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")
        self.env_mock = Mock(name="env")

    @patch("cloud_components.infra.aws.builder.AwsBuilder")
    def test_manufacture_aws__call_aws_builder_with_logger_and_env_mock__expected_one_call(
        self, aws_builder_mock: Mock
    ):
        instance = InfraFactory(logger=self.logger_mock)
        instance.manufacture_aws(
            access_key="lol",
            secret_access_key="abcdefgh",
            env="local",
            localstack_url="http://localhost:4566",
        )

        aws_builder_mock.assert_called_once_with(
            self.logger_mock, "lol", "abcdefgh", "local", "http://localhost:4566"
        )
