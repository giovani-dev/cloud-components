from google.cloud import storage
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.repository.cloud_storage import CloudStorage


class StorageFactory(IFactory[IStorage]):
    """Factory building Cloud Storage repository implementations."""

    def __init__(self, logger: ILogger) -> None:
        """Persist the logger instance."""
        self.logger = logger

    def manufacture(self) -> IStorage:
        """Return a configured :class:`CloudStorage` instance."""
        return CloudStorage(connection=storage.Client(), logger=self.logger)
