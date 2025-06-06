from google.cloud import pubsub_v1
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.repository.pub_sub import PubSub


class EventFactory(IFactory[IEvent]):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture(self) -> IEvent:
        return PubSub(connection=pubsub_v1.PublisherClient(), logger=self.logger)
