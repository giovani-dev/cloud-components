from unittest.mock import Mock, patch

from cloud_components.services.env.dotenv import Dotenv


class TestDotEnv:
    logger_mock: Mock

    def setup_method(self):
        self.logger_mock = Mock(name="logger")

    @patch("dotenv.load_dotenv")
    def test_load__cannot_find_dotenv__expected_import_error(  # pylint: disable=C0116,C0301
        self, load_dotenv_mock: Mock
    ):
        load_dotenv_mock.side_effect = ImportError("test error...")

        instance = Dotenv(log=self.logger_mock)
        instance.load()

        self.logger_mock.info.assert_called_once_with("Loading enviroment variables")
        self.logger_mock.error.assert_called_once_with(
            "An error occurred when try to load dotenv lib. Error detail: test error..."
        )

    @patch("dotenv.load_dotenv")
    def test_load__call_load_dotenv_function__expected_call_with_errors(  # pylint: disable=C0116,C0301
        self, load_dotenv_mock: Mock
    ):
        instance = Dotenv(log=self.logger_mock)
        instance.load()

        load_dotenv_mock.assert_called()
        self.logger_mock.info.assert_called_once_with("Loading enviroment variables")

    @patch("os.getenv")
    def test_get__get_env_without_cast_value__expected_cast_not_call(
        self, getenv_mock: Mock
    ):
        env_name = "test_env"

        instance = Dotenv(log=self.logger_mock)
        instance.get(env_name)

        getenv_mock.assert_called_once_with(env_name, None)

    @patch("os.getenv")
    def test_get__casting_value__expected_cast_call(self, getenv_mock: Mock):
        env_name = "test_env"
        cast_mock = Mock(name="cast")

        instance = Dotenv(log=self.logger_mock)
        instance.get(env_name, cast_mock)

        getenv_mock.assert_called_once_with(env_name, None)
