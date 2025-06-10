import os
from typing import Any, Callable, Union

from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger

try:
    from dotenv import load_dotenv
except ImportError as err:  # pragma: no cover - handled at runtime
    raise ImportError(
        "The 'python-dotenv' package is required to load environment variables"
    ) from err


class Dotenv(IEnviroment):
    """Implementation of :class:`IEnviroment` using ``python-dotenv``."""

    def __init__(self, logger: ILogger) -> None:
        """Initialize the loader with the given logger."""
        self.logger = logger

    def load(self) -> None:
        """Load variables from a ``.env`` file into the process environment."""
        self.logger.info("Loading enviroment variables")
        load_dotenv()

    def get(
        self,
        env_name: str,
        cast: Union[Callable[[Any], Any], None] = None,
        default: Union[Any, None] = None,
    ) -> Any:
        """Return the environment variable ``env_name`` casted to ``cast``."""
        value = os.getenv(env_name, defalt)
        return value if not cast else cast(value)
