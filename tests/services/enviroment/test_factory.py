from unittest.mock import Mock, patch

from cloud_components.services.enviroment.factory import EnvFactory


class TestEnvFactory:
    logger_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")

    @patch("cloud_components.services.enviroment.factory.Dotenv")
    def test_manufacture_dotenv__call_dotenv_class__expected_dotenv_constructor_call_with_logger_mock(  # pylint: disable=C0116,C0301
        self, dotenv_mock: Mock
    ):
        instance = EnvFactory(logger=self.logger_mock)
        instance.manufacture_dotenv()

        dotenv_mock.assert_called_once_with(log=self.logger_mock)
