from typing import Any, Union
from google.cloud import tasks_v2
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.libs.logger import ILogger


class CloudTasks(IQueue):
    _queue: Union[str, None] = None

    def __init__(self, connection: tasks_v2.CloudTasksClient, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def queue(self) -> Any:
        if not self._queue:
            raise ResourceNameNotFound("Queue not found, please provide a name to it")
        return self._queue

    @queue.setter
    def queue(self, value: str):
        self._queue = value

    def send_message(self, message: str) -> bool:
        raise NotImplementedError

    def receive_message(self) -> str:
        raise NotImplementedError
