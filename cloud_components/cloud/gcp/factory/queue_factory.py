from google.cloud import tasks_v2
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.repository.cloud_tasks import CloudTasks


class QueueFactory(IFactory[IQueue]):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture(self) -> IQueue:
        return CloudTasks(connection=tasks_v2.CloudTasksClient(), logger=self.logger)
