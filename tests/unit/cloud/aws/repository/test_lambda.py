import pytest
from unittest.mock import Mock

from cloud_components.cloud.aws.repository.lambda_function import Lambda
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound


class TestLambda:
    def setup_method(self):
        self.connection = Mock()
        self.logger = Mock()
        self.instance = Lambda(connection=self.connection, logger=self.logger)

    def test_function_getter_without_set_raises(self):
        """Accessing function before setting it should raise an error."""
        with pytest.raises(ResourceNameNotFound):
            _ = self.instance.function

    def test_function_setter_and_getter(self):
        """Ensure the function name can be set and retrieved."""
        self.instance.function = "my-function"
        assert self.instance.function == "my-function"

    def test_execute_not_implemented(self):
        """Lambda base class should have abstract execute implementation."""
        with pytest.raises(NotImplementedError):
            self.instance.execute(b"payload")
