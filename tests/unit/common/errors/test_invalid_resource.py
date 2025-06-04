from cloud_components.common.errors.invalid_resource import InvalidResource, ResourceNameNotFound


def test_exception_inheritance():
    """Ensure custom exceptions inherit from ``Exception``."""
    assert issubclass(InvalidResource, Exception)
    assert issubclass(ResourceNameNotFound, Exception)
