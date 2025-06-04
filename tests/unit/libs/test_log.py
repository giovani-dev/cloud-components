from unittest.mock import Mock, patch

from cloud_components.libs.log.log import Loguru


class TestLoguru:
    """Tests for the Loguru helper"""

    def test_load_returns_logger(self):
        """load() should return the loguru logger instance"""
        fake_logger = Mock(name="logger")
        with patch("cloud_components.libs.log.log.logger", fake_logger):
            assert Loguru().load() is fake_logger
