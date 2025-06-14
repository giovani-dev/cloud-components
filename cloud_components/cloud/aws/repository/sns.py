import json
from typing import Any, Literal, Union
from botocore.exceptions import ClientError
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.libs.logger import ILogger


class Sns(IEvent):
    """Amazon SNS implementation of :class:`IEvent`."""

    _source: Union[str, None] = None

    def __init__(self, connection: Any, logger: ILogger):
        """Instantiate the repository with an SNS client and logger."""
        self.connection = connection
        self.logger = logger

    @property
    def source(self) -> Any:
        """Return the SNS topic ARN."""
        if not self._source:
            raise ResourceNameNotFound(
                "Sns Source not found, please provide a name to it"
            )
        return self._source

    @source.setter
    def source(self, value: str) -> None:
        """Set the SNS topic ARN."""
        self._source = value

    def send(
        self, message: dict, message_structere: Union[Literal["json"], None] = None
    ) -> bool:
        """Send a ``message`` to the configured SNS topic."""
        try:
            if message_structere:
                self.connection.publish(
                    TargetArn=self.source,
                    Message=json.dumps({"default": json.dumps(message)}),
                    MessageStructure=message_structere,
                )
            else:
                self.connection.publish(
                    TargetArn=self.source,
                    Message=json.dumps(message),
                )
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to send a message. Error detail: {err}"
            )
            return False
        return True
