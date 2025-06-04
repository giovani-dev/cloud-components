from unittest.mock import Mock, patch

from cloud_components.cloud.aws.facade import AWSFacade


class TestAWSFacade:
    logger: Mock
    env: Mock
    instance: AWSFacade

    def setup_method(self):
        self.logger = Mock(name="logger")
        self.env = Mock(name="env")
        self.instance = AWSFacade(logger=self.logger, env=self.env)

    @patch("cloud_components.cloud.aws.facade.Eventfactory")
    def test_event_returns_implementation(self, event_factory: Mock):
        """Return value from ``event`` should come from the factory."""
        event = Mock(name="event")
        factory = Mock(name="factory")
        event_factory.return_value = factory
        factory.manufacture.return_value = event

        callback = self.instance.event()

        assert callback is event
        event_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.FunctionFactory")
    def test_function_returns_implementation(self, func_factory: Mock):
        """``function`` should create and return a Lambda repository."""
        function = Mock(name="function")
        factory = Mock(name="factory")
        func_factory.return_value = factory
        factory.manufacture.return_value = function

        callback = self.instance.function()

        assert callback is function
        func_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.QueueFactory")
    def test_queue_returns_implementation(self, queue_factory: Mock):
        """``queue`` should create and return a queue repository."""
        queue = Mock(name="queue")
        factory = Mock(name="factory")
        queue_factory.return_value = factory
        factory.manufacture.return_value = queue

        callback = self.instance.queue()

        assert callback is queue
        queue_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.StorageFactory")
    def test_storage_returns_implementation(self, storage_factory: Mock):
        """``storage`` should create and return an S3 repository."""
        storage = Mock(name="storage")
        factory = Mock(name="factory")
        storage_factory.return_value = factory
        factory.manufacture.return_value = storage

        callback = self.instance.storage()

        assert callback is storage
        storage_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()
