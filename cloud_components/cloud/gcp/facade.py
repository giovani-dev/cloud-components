from cloud_components.common.interface.facade import ICloudFacade
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.factory.storage_factory import StorageFactory
from cloud_components.cloud.gcp.factory.event_factory import EventFactory
from cloud_components.cloud.gcp.factory.function_factory import FunctionFactory
from cloud_components.cloud.gcp.factory.queue_factory import QueueFactory


class GCSFacade(ICloudFacade):
    """Facade exposing Google Cloud services."""

    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        """Save logger and environment references."""
        self.logger = logger
        self.env = env

    def event(self) -> IEvent:
        return EventFactory(logger=self.logger).manufacture()

    def function(self) -> IFunction:
        return FunctionFactory(logger=self.logger).manufacture()

    def queue(self) -> IQueue:
        return QueueFactory(logger=self.logger).manufacture()

    def storage(self) -> IStorage:
        """Return a Cloud Storage repository instance."""
        return StorageFactory(logger=self.logger).manufacture()
