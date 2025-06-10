from abc import ABC, abstractmethod
from typing import Any, Literal


class IEvent(ABC):
    """Interface that defines a publish/subscribe event source."""

    @property
    @abstractmethod
    def source(self) -> Any:
        """Return the current event source."""
        raise NotImplementedError

    @source.setter
    @abstractmethod
    def source(self, value: str) -> str:
        """Set the current event source."""
        raise NotImplementedError

    @abstractmethod
    def send(self, message: dict, message_structere: Literal["json"] = "json") -> bool:
        """Send ``message`` using the underlying provider."""
        raise NotImplementedError
