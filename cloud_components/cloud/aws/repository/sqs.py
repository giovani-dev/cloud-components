from typing import Any, Union
from botocore.exceptions import ClientError
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.libs.logger import ILogger


class Sqs(IQueue):
    """Amazon SQS implementation of :class:`IQueue`."""

    _queue: Union[str, None] = None
    _queue_name: Union[str, None] = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        """Initialize the repository with a boto3 resource and logger."""
        self.connection = connection
        self.logger = logger

    @property
    def queue(self) -> Any:
        """Return the SQS queue resource."""
        if not self._queue:
            raise ResourceNameNotFound("Queue not found, please provide a name to it")
        return self._queue

    @queue.setter
    def queue(self, value: str) -> None:
        """Set the SQS queue by name."""
        self._queue_name = value
        self._queue = self.connection.get_queue_by_name(QueueName=value)

    def send_message(self, message: str) -> bool:
        """Send a ``message`` to the queue."""
        try:
            self.queue.send_message(MessageBody=message)
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to send a message. Error detail: {err}"
            )
            return False
        return True

    def receive_message(self) -> str:
        """Receive a message from the queue."""
        raise NotImplementedError
