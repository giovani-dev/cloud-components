from typing import cast
from cloud_components.common.interface.libs.logger import ILogger

try:
    from loguru import logger
except ImportError as err:  # pragma: no cover - handled at runtime
    raise ImportError("The 'loguru' package is required for logging") from err


class Loguru:
    """Simple wrapper around :mod:`loguru` exposing an :class:`ILogger`."""

    def load(self) -> ILogger:
        """Return the configured :class:`ILogger` instance."""
        return cast(ILogger, logger)
