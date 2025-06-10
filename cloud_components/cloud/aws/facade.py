from cloud_components.common.interface.facade import ICloudFacade
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.enviroment import IEnvironment
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.aws.factory.event_factory import Eventfactory
from cloud_components.cloud.aws.factory.function_factory import FunctionFactory
from cloud_components.cloud.aws.factory.queue_factory import QueueFactory
from cloud_components.cloud.aws.factory.storage_factory import StorageFactory


class AWSFacade(ICloudFacade):
    """Concrete facade for AWS services."""

    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        """Store the logger and environment configuration."""
        self.logger = logger
        self.env = env

    def event(self) -> IEvent:
        """Return an SNS event repository instance."""
        return Eventfactory(self.logger, self.env).manufacture()

    def function(self) -> IFunction:
        """Return a Lambda function repository instance."""
        return FunctionFactory(self.logger, self.env).manufacture()

    def queue(self) -> IQueue:
        """Return an SQS queue repository instance."""
        return QueueFactory(self.logger, self.env).manufacture()

    def storage(self) -> IStorage:
        """Return an S3 storage repository instance."""
        return StorageFactory(self.logger, self.env).manufacture()
