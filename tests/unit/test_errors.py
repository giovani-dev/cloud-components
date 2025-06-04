from cloud_components.common.errors.invalid_resource import InvalidResource, ResourceNameNotFound


def test_error_classes_can_be_instantiated():
    """Ensure custom exceptions can be instantiated"""
    assert isinstance(InvalidResource("msg"), InvalidResource)
    assert isinstance(ResourceNameNotFound("msg"), ResourceNameNotFound)

