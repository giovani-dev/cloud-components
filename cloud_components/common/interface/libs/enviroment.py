from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class IEnvironment(ABC):  # pylint: disable=C0115
    @abstractmethod
    def load(self) -> None:  # pylint: disable=C0116
        raise NotImplementedError

    @abstractmethod
    def get(  # pylint: disable=C0116
        self,
        env_name: str,
        cast: Union[Callable[[Any], Any], None] = None,
        default: Union[Any, None] = None,
    ) -> Any:
        raise NotImplementedError
