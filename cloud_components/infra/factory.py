from typing import Literal, Union
from cloud_components.application.interface.infra.builder import IBuilder
from cloud_components.application.interface.services.log.logger import ILogger


class InfraFactory:
    """
    This class manufacture cloud implementations from infra package,
    every implementation has a builder class to make more simple your
    declaration, and all this is encapsulated in manufacture methods.

    ...

    Attributes
    ----------
    logger : ILogger
        blabla
    env : IEnviroment
        blabla

    Methods
    ----------
    manufacture_aws()
        This method import and construct an AwsBuilder class. I decided
        to import the package here because the boto3 package is to much
        slow in terms of import.
    """

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture_aws(
        self,
        access_key: str,
        secret_access_key: str,
        env: Union[Literal["local"], None] = None,
        localstack_url: Union[str, None] = None,
    ) -> IBuilder:
        """
        Returns
        ----------
        IBuilder
            An IBuilder implemetation called AwsBuilder
        """
        self.logger.info("Manufacturing AwsBuilder class")
        from cloud_components.infra.aws.builder import (  # pylint: disable=C0415
            AwsBuilder,
        )

        return AwsBuilder(
            self.logger, access_key, secret_access_key, env, localstack_url
        )

    def manufacture_gcp(self) -> IBuilder:
        self.logger.info("Manufacturing GcpBuilder class")
        from cloud_components.infra.gcp.builder import (  # pylint: disable=C0415
            GcpBuilder,
        )

        return GcpBuilder(self.logger)
