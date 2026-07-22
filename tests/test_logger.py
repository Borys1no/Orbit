"""Tests for orbit.core.logger."""

import logging

from orbit.core.logger import _reset, get_logger, setup_logging


def test_get_logger_returns_child():
    _reset()
    logger = get_logger("weather")
    assert logger.name == "orbit.weather"
    assert isinstance(logger, logging.Logger)


def test_setup_logging_configures_root():
    _reset()
    setup_logging(level=logging.DEBUG)
    root = logging.getLogger("orbit")
    assert root.level == logging.DEBUG


def test_setup_logging_idempotent():
    _reset()
    setup_logging(level=logging.WARNING)
    setup_logging(level=logging.DEBUG)
    root = logging.getLogger("orbit")
    assert root.level == logging.WARNING
