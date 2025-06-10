from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IFactory(ABC, Generic[T]):
    """Generic factory interface."""

    @abstractmethod
    def manufacture(self) -> T:
        """Return a new instance of ``T``."""
        raise NotImplementedError
