from unittest.mock import Mock, patch

from cloud_components.services.log.builder import LogBuilder


class TestLogBuilderUnit:
    @patch("cloud_components.services.log.builder.ILogger")
    @patch("cloud_components.services.log.builder.cast")
    @patch("loguru.logger")
    def test_build_loguru_method__should_cast_logger_to_log_interface(
        self, logger: Mock, cast: Mock, logger_interface: Mock
    ):
        builder = LogBuilder()
        builder.build_loguru()

        cast.assert_called_once_with(logger_interface, logger)
