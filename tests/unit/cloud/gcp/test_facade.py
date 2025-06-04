from unittest.mock import Mock, patch
import pytest

from cloud_components.cloud.gcp.facade import GCSFacade


class TestGCSFacade:
    def setup_method(self):
        self.logger = Mock()
        self.env = Mock()
        self.instance = GCSFacade(logger=self.logger, env=self.env)

    def test_event_not_implemented(self):
        """Calling ``event`` is not implemented for GCP facade."""
        with pytest.raises(NotImplementedError):
            self.instance.event()

    def test_function_not_implemented(self):
        """Calling ``function`` should raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            self.instance.function()

    def test_queue_not_implemented(self):
        """Queue access is not available in the GCP facade."""
        with pytest.raises(NotImplementedError):
            self.instance.queue()

    @patch('cloud_components.cloud.gcp.facade.StorageFactory')
    def test_storage_returns_instance(self, factory_cls: Mock):
        """``storage`` should return the repository created by the factory."""
        factory = factory_cls.return_value
        storage = Mock()
        factory.manufacture.return_value = storage
        result = self.instance.storage()
        assert result is storage
        factory_cls.assert_called_once_with(logger=self.logger)
        factory.manufacture.assert_called_once_with()
