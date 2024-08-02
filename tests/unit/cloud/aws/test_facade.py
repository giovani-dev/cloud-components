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
    def test_should_event_manufacture_an_event_implementation(
        self, event_factory: Mock
    ):
        event = Mock(name="event")
        factory = Mock(name="factory")
        event_factory.return_value = factory
        factory.manufacture.return_value = event

        callback = self.instance.event()

        assert callback is event
        event_factory.assert_called_once_with(self.logger, self.env)
        factory.manufacture.assert_called_once_with()

    
