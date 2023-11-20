from cloud_components.application.interface.services.enviroment import IEnviroment
from cloud_components.application.interface.services.log import ILog
from cloud_components.services.enviroment.dotenv import Dotenv


class EnvFactory:
    def __init__(self, logger: ILog) -> None:
        self.logger = logger

    def manufacture_dotenv(self) -> IEnviroment:
        return Dotenv(log=self.logger)
