from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.application.types.gcp import ResourceType
from cloud_components.infra.gcp.connection.connector_factory import ConnectorFactory


class ResourceConnector:
    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.logger = logger

    def connect(self, resource_name: ResourceType):
        return ConnectorFactory.manufacture(resource_name)
