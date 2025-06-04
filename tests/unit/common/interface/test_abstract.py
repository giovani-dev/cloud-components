import pytest

from cloud_components.common.interface.facade import ICloudFacade
from cloud_components.common.interface.factory import IFactory


def test_abstract_facade_cannot_instantiate():
    """Interfaces should not be instantiated directly."""
    with pytest.raises(TypeError):
        ICloudFacade()


def test_abstract_factory_cannot_instantiate():
    """Subclasses of IFactory must implement manufacture."""
    class MyFactory(IFactory[int]):
        pass

    with pytest.raises(TypeError):
        MyFactory()
