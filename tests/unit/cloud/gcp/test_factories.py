from unittest.mock import Mock, patch

from cloud_components.cloud.gcp.factory.event_factory import EventFactory
from cloud_components.cloud.gcp.factory.function_factory import FunctionFactory
from cloud_components.cloud.gcp.factory.queue_factory import QueueFactory


class TestEventFactory:
    def test_manufacture_returns_pubsub_repository(self):
        logger = Mock(name="logger")
        with patch(
            "cloud_components.cloud.gcp.factory.event_factory.pubsub_v1.PublisherClient"
        ) as client_cls, patch(
            "cloud_components.cloud.gcp.factory.event_factory.PubSub"
        ) as repo_cls:
            client = Mock(name="client")
            repo = Mock(name="repo")
            client_cls.return_value = client
            repo_cls.return_value = repo

            factory = EventFactory(logger=logger)
            result = factory.manufacture()

            assert result is repo
            client_cls.assert_called_once_with()
            repo_cls.assert_called_once_with(connection=client, logger=logger)


class TestFunctionFactory:
    def test_manufacture_returns_cloud_function_repository(self):
        logger = Mock(name="logger")
        with patch(
            "cloud_components.cloud.gcp.factory.function_factory.functions_v1.CloudFunctionsServiceClient"
        ) as client_cls, patch(
            "cloud_components.cloud.gcp.factory.function_factory.CloudFunction"
        ) as repo_cls:
            client = Mock(name="client")
            repo = Mock(name="repo")
            client_cls.return_value = client
            repo_cls.return_value = repo

            factory = FunctionFactory(logger=logger)
            result = factory.manufacture()

            assert result is repo
            client_cls.assert_called_once_with()
            repo_cls.assert_called_once_with(connection=client, logger=logger)


class TestQueueFactory:
    def test_manufacture_returns_cloud_tasks_repository(self):
        logger = Mock(name="logger")
        with patch(
            "cloud_components.cloud.gcp.factory.queue_factory.tasks_v2.CloudTasksClient"
        ) as client_cls, patch(
            "cloud_components.cloud.gcp.factory.queue_factory.CloudTasks"
        ) as repo_cls:
            client = Mock(name="client")
            repo = Mock(name="repo")
            client_cls.return_value = client
            repo_cls.return_value = repo

            factory = QueueFactory(logger=logger)
            result = factory.manufacture()

            assert result is repo
            client_cls.assert_called_once_with()
            repo_cls.assert_called_once_with(connection=client, logger=logger)
