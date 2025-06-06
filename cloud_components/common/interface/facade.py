from abc import ABC, abstractmethod

from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage


class ICloudFacade(ABC):
    """High level interface for cloud service facades."""

    @abstractmethod
    def event(self) -> IEvent:
        """Return an event repository implementation."""
        raise NotImplementedError

    @abstractmethod
    def function(self) -> IFunction:
        """Return a function repository implementation."""
        raise NotImplementedError

    @abstractmethod
    def queue(self) -> IQueue:
        """Return a queue repository implementation."""
        raise NotImplementedError

    @abstractmethod
    def storage(self) -> IStorage:
        """Return a storage repository implementation."""
        raise NotImplementedError
