from google.cloud import functions_v1
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.repository.cloud_function import CloudFunction


class FunctionFactory(IFactory[IFunction]):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture(self) -> IFunction:
        return CloudFunction(
            connection=functions_v1.CloudFunctionsServiceClient(), logger=self.logger
        )
