import pytest
from unittest.mock import Mock, patch

from cloud_components.cloud.gcp.facade import GCSFacade


class TestGCSFacade:
    """Tests for the GCSFacade methods"""

    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.instance = GCSFacade(logger=self.logger, env=self.env)

    def test_unimplemented_methods(self):
        """event, function and queue should raise NotImplementedError"""
        with pytest.raises(NotImplementedError):
            self.instance.event()
        with pytest.raises(NotImplementedError):
            self.instance.function()
        with pytest.raises(NotImplementedError):
            self.instance.queue()

    @patch("cloud_components.cloud.gcp.facade.StorageFactory")
    def test_storage_returns_manufactured_storage(self, factory_cls: Mock):
        """storage() should manufacture storage using StorageFactory"""
        storage = Mock()
        factory = Mock()
        factory_cls.return_value = factory
        factory.manufacture.return_value = storage

        result = self.instance.storage()

        assert result is storage
        factory_cls.assert_called_once_with(logger=self.logger)
        factory.manufacture.assert_called_once_with()

