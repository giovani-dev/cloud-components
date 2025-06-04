from unittest.mock import Mock, patch

from cloud_components.cloud.aws.facade import AWSFacade


class TestAWSFacade:
    logger: Mock
    env: Mock
    instance: Mock

    def setup_method(self):
        self.logger = Mock(name="logger")
        self.env = Mock(name="env")
        self.instance = AWSFacade(logger=self.logger, env=self.env)

    @patch("cloud_components.cloud.aws.facade.Eventfactory")
    def test_should_event_manufacture_an_event_implementation(self, event_factory: Mock):
        """event() should build an event implementation via Eventfactory"""
        event = Mock(name="event")
        factory = Mock(name="factory")
        event_factory.return_value = factory
        factory.manufacture.return_value = event

        callback = self.instance.event()

        assert callback is event
        event_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.FunctionFactory")
    def test_function_returns_manufactured_function(self, factory_cls: Mock):
        """function() should build a function implementation via FunctionFactory"""
        function = Mock(name="func")
        factory = Mock(name="factory")
        factory_cls.return_value = factory
        factory.manufacture.return_value = function

        result = self.instance.function()

        assert result is function
        factory_cls.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.QueueFactory")
    def test_queue_returns_manufactured_queue(self, factory_cls: Mock):
        """queue() should build a queue implementation via QueueFactory"""
        queue = Mock(name="queue")
        factory = Mock(name="factory")
        factory_cls.return_value = factory
        factory.manufacture.return_value = queue

        result = self.instance.queue()

        assert result is queue
        factory_cls.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    @patch("cloud_components.cloud.aws.facade.StorageFactory")
    def test_storage_returns_manufactured_storage(self, factory_cls: Mock):
        """storage() should build a storage implementation via StorageFactory"""
        storage = Mock(name="storage")
        factory = Mock(name="factory")
        factory_cls.return_value = factory
        factory.manufacture.return_value = storage

        result = self.instance.storage()

        assert result is storage
        factory_cls.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

