from abc import ABC, abstractmethod


class IFunction(ABC):
    """Interface for cloud function invocations."""

    @property
    @abstractmethod
    def function(self):
        """Return the function identifier."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, payload: bytes):
        """Execute the function with the provided payload."""
        raise NotImplementedError
