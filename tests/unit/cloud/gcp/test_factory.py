from unittest.mock import Mock, patch

from cloud_components.cloud.gcp.factory.storage_factory import StorageFactory


class TestStorageFactory:
    """StorageFactory.manufacture"""

    def test_manufacture_builds_cloud_storage(self):
        logger = Mock()
        client = Mock()
        with patch("google.cloud.storage.Client", return_value=client) as client_cls:
            result = StorageFactory(logger=logger).manufacture()
            assert result.connection is client
            client_cls.assert_called_once_with()

