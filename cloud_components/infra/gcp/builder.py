from cloud_components.application.interface.infra.builder import IBuilder
from cloud_components.application.interface.infra.event import IEvent
from cloud_components.application.interface.infra.function import IFunction
from cloud_components.application.interface.infra.queue import IQueue
from cloud_components.application.interface.infra.storage import IStorage
from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.infra.gcp.connection.resource_connector import ResourceConnector
from cloud_components.infra.gcp.resources.storage import CloudStorage


class GcpBuilder(IBuilder):
    def __init__(self, logger: ILogger) -> None:
        self.resource = ResourceConnector(logger)
        self.logger = logger

    def build_storage(self) -> IStorage:
        self.logger.info("Building cloud storage implementation")
        connection = self.resource.connect("CloudStorage")
        return CloudStorage(connection=connection, logger=self.logger)

    def build_function(self) -> IFunction:
        raise NotImplementedError

    def build_queue(self) -> IQueue:
        raise NotImplementedError

    def build_event(self) -> IEvent:
        raise NotImplementedError
