from abc import ABC, abstractmethod


class ILogger(ABC):
    """Interface used by the library for logging."""

    @abstractmethod
    def debug(self, message: str) -> None:
        """Log ``message`` with debug severity."""
        raise NotADirectoryError

    @abstractmethod
    def info(self, message: str) -> None:
        """Log ``message`` with info severity."""
        raise NotADirectoryError

    @abstractmethod
    def success(self, message: str) -> None:
        """Log ``message`` with success severity."""
        raise NotADirectoryError

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log ``message`` with warning severity."""
        raise NotADirectoryError

    @abstractmethod
    def error(self, message: str) -> None:
        """Log ``message`` with error severity."""
        raise NotADirectoryError
