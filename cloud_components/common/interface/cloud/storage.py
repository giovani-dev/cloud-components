from abc import ABC, abstractmethod
from typing import Any, Union


class IStorage(ABC):
    """Interface describing basic storage operations."""

    @abstractmethod
    def save_file(
        self,
        data: bytes,
        file_path: str,
        content_type: str,
        is_public: bool = False,
    ) -> bool:
        """Persist ``data`` at ``file_path``."""
        raise NotImplementedError

    @abstractmethod
    def get_file(self, file_path: str) -> Union[bytes, None]:
        """Return the bytes stored at ``file_path``."""
        raise NotImplementedError

    @property
    @abstractmethod
    def bucket(self) -> Any:
        """Return the storage bucket resource."""
        raise NotImplementedError

    @bucket.setter
    @abstractmethod
    def bucket(self, name: str) -> None:
        """Set the active bucket by ``name``."""
        raise NotImplementedError

    @abstractmethod
    def ls(self, path: str) -> list[str]:  # pylint: disable=C0103
        """List files stored under ``path``."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        """Remove ``file_path`` from storage."""
        raise NotImplementedError
