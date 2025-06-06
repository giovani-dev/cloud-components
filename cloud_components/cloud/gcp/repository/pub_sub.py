import json
from typing import Any, Literal, Union
from google.cloud import pubsub_v1
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.libs.logger import ILogger


class PubSub(IEvent):
    _source: Union[str, None] = None

    def __init__(self, connection: pubsub_v1.PublisherClient, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def source(self) -> Any:
        if not self._source:
            raise ResourceNameNotFound(
                "PubSub topic not found, please provide a name to it"
            )
        return self._source

    @source.setter
    def source(self, value: str):
        self._source = value

    def send(self, message: dict, message_structere: Literal["json"] = "json") -> bool:
        try:
            data = json.dumps(message).encode("utf-8")
            future = self.connection.publish(self.source, data=data)
            future.result()
        except Exception as err:  # pylint: disable=W0718
            self.logger.error(
                f"An error occurred when try to send a message. Error detail: {err}"
            )
            return False
        return True
