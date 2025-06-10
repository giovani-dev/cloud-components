from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class IEnviroment(ABC):
    """Interface to load and retrieve environment variables."""

    @abstractmethod
    def load(self) -> None:
        """Load environment variables from an external source."""
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        env_name: str,
        cast: Union[Callable[[Any], Any], None] = None,
        default: Union[Any, None] = None,
    ) -> Any:
        """Return ``env_name`` optionally cast to ``cast``."""
        raise NotImplementedError
