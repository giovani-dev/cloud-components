import boto3

from cloud_components.cloud.aws.repository.sns import Sns
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.common.interface.libs.enviroment import IEnvironment


class Eventfactory(IFactory[IEvent]):
    """Factory responsible for building SNS event repositories."""

    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        """Initialize the factory with its dependencies."""
        self.logger = logger
        self.env = env

    def manufacture(self) -> IEvent:
        """Return a configured :class:`Sns` repository instance."""
        connection = boto3.client(
            "sns",
            aws_access_key_id=self.env.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=self.env.get("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=self.env.get("AWS_ENDPOINT_URL"),
        )
        return Sns(connection=connection, logger=self.logger)
