from unittest.mock import Mock, patch

from cloud_components.libs.env.env import Dotenv


class TestDotenv:
    @patch('cloud_components.libs.env.env.load_dotenv', create=True)
    def test_load_calls_dotenv(self, load_dotenv: Mock):
        """load should invoke ``load_dotenv`` and log the action."""
        logger = Mock()
        env = Dotenv(logger=logger)
        env.load()
        logger.info.assert_called_once_with("Loading enviroment variables")
        load_dotenv.assert_called_once_with()

    @patch('cloud_components.libs.env.env.os')
    def test_get_returns_env_value(self, os_mod: Mock):
        """get should return the value of an environment variable."""
        os_mod.getenv.return_value = 'value'
        env = Dotenv(logger=Mock())
        assert env.get('NAME') == 'value'
        os_mod.getenv.assert_called_once_with('NAME', None)

    @patch('cloud_components.libs.env.env.os')
    def test_get_casts_value(self, os_mod: Mock):
        """get should cast the value when a type is provided."""
        os_mod.getenv.return_value = '1'
        env = Dotenv(logger=Mock())
        result = env.get('NUMBER', int)
        assert result == 1
        os_mod.getenv.assert_called_once_with('NUMBER', None)
