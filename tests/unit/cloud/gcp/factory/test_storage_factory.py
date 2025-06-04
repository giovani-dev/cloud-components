from unittest.mock import Mock, patch

from cloud_components.cloud.gcp.factory.storage_factory import StorageFactory


@patch('cloud_components.cloud.gcp.factory.storage_factory.storage')
class TestGCPStorageFactory:
    def test_manufacture_returns_cloud_storage(self, storage_mod: Mock):
        """Factory should create a CloudStorage repository."""
        client = storage_mod.Client.return_value
        factory = StorageFactory(logger=Mock())
        storage_instance = factory.manufacture()
        assert storage_instance.connection is client
        storage_mod.Client.assert_called_once_with()
