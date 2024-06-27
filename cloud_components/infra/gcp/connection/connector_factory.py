from google.cloud import storage
from cloud_components.application.errors.invalid_resource import InvalidResource
from cloud_components.application.types.gcp import ResourceType


class ConnectorFactory:
    @staticmethod
    def manufacture(resource: ResourceType):
        if resource == "CloudStorage":
            return storage.Client()
        raise InvalidResource
