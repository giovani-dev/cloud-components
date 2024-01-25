from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.infra.aws.builder import AwsBuilder
from cloud_components.infra.factory import InfraFactory
from cloud_components.services.log.builder import LogBuilder


class TestInfraFactoryIntegration:
    logger: ILogger

    def setup_class(self):
        self.logger = LogBuilder().build_loguru()

    def test_manufacture_aws_method__should_manufacture_builder__expected_aws_builder_instance(
        self,
    ):  # pylint: disable=C0301
        factory = InfraFactory(logger=self.logger)

        builder = factory.manufacture_aws(
            access_key="test-key",
            secret_access_key="test-secret-key",
            env="local",
            localstack_url="http://localhost:4566",
        )

        assert isinstance(builder, AwsBuilder)
