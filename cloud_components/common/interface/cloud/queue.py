from abc import ABC, abstractmethod
from typing import Any


class IQueue(ABC):
    """Interface that defines queue behaviour."""

    @property
    @abstractmethod
    def queue(self) -> Any:
        """Return the underlying queue resource."""
        raise NotImplementedError

    @queue.setter
    @abstractmethod
    def queue(self, value: str) -> None:
        """Set the queue resource by name."""
        raise NotImplementedError

    @abstractmethod
    def send_message(self, message: str) -> bool:
        """Send ``message`` to the queue."""
        raise NotImplementedError

    @abstractmethod
    def receive_message(self) -> str:
        """Receive a single message from the queue."""
        raise NotImplementedError
