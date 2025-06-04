from unittest.mock import Mock, patch

from cloud_components.libs.log.log import Loguru


class TestLoguru:
    @patch('cloud_components.libs.log.log.logger')
    def test_load_returns_logger(self, logger_mock: Mock):
        """load should return the configured loguru logger."""
        instance = Loguru()
        result = instance.load()
        assert result is logger_mock
