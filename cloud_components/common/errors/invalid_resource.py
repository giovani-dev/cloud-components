class InvalidResource(Exception):
    """Base exception for invalid cloud resources."""

    def __init__(self, *args: object) -> None:
        """Create the exception with the provided arguments."""
        super().__init__(*args)


class ResourceNameNotFound(Exception):
    """Raised when a required resource name is missing."""

    def __init__(self, *args: object) -> None:
        """Create the exception with the provided arguments."""
        super().__init__(*args)
