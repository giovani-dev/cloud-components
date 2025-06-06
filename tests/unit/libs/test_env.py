import os
from unittest.mock import Mock, patch

from cloud_components.libs.env.env import Dotenv


class TestDotenv:
    """Tests for Dotenv environment helper"""

    def setup_method(self):
        self.logger = Mock()
        self.instance = Dotenv(logger=self.logger)

    def test_load_calls_logger_and_load_dotenv(self):
        """load() should log and invoke load_dotenv"""
        with patch("cloud_components.libs.env.env.load_dotenv") as load:
            self.instance.load()
            load.assert_called_once_with()
            self.logger.info.assert_called_once_with("Loading enviroment variables")

    def test_get_returns_value_without_cast(self):
        """get() should return the environment variable value without casting"""
        with patch.dict(os.environ, {"TEST_VAR": "value"}):
            assert self.instance.get("TEST_VAR") == "value"

    def test_get_applies_cast_and_default(self):
        """get() should cast the value and return default when missing"""
        with patch.dict(os.environ, {}, clear=True):
            result = self.instance.get("MISSING", cast=int, defalt="10")
            assert result == 10
