import pytest
from unittest.mock import Mock

from botocore.exceptions import ClientError
from cloud_components.cloud.aws.repository.sns import Sns
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestSns:
    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.instance = Sns(connection=self.connection, logger=self.logger)

    def test_source_property_without_set(self):
        """Accessing ``source`` before setting should raise an error."""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.source

    def test_source_setter(self):
        """Setting ``source`` should store the provided ARN."""
        self.instance.source = "arn"
        assert self.instance.source == "arn"

    def test_send_success_default(self):
        """send should publish a message with default structure."""
        self.instance.source = "arn"
        assert self.instance.send({"a": 1})
        self.connection.publish.assert_called_once()

    def test_send_success_with_structure(self):
        """send should allow specifying a message structure."""
        self.instance.source = "arn"
        assert self.instance.send({"a": 1}, "json")
        self.connection.publish.assert_called()

    def test_send_failure_returns_false(self):
        """Failures when publishing should return ``False`` and log."""
        self.instance.source = "arn"
        self.connection.publish.side_effect = ClientError({}, "publish")
        assert not self.instance.send({})
        self.logger.error.assert_called_once()
