from typing import Any, Union
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.libs.logger import ILogger


class Lambda(IFunction):
    """Wrapper around AWS Lambda functions."""

    _name: Union[str, None] = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        """Initialize with a boto3 client and logger."""
        self.connection = connection
        self.logger = logger

    @property
    def function(self):
        """Return the configured Lambda function name."""
        if not self._name:
            raise ResourceNameNotFound(
                "Function not found, please provide a name to it"
            )
        return self._name

    @function.setter
    def function(self, value: str) -> None:
        """Set the Lambda function name."""
        self._name = value

    def execute(self, payload: bytes):
        try:
            response = self.connection.invoke(
                FunctionName=self.function,
                Payload=payload,
            )
            result = response.get("Payload")
            if hasattr(result, "read"):
                return result.read()
            return result
        except Exception as err:  # pylint: disable=W0718
            self.logger.error(
                f"An error occurred when try to execute a function. Error detail: {err}"
            )
            return None
