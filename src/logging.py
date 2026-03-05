import logging
import os
from typing import Any

from pythonjsonlogger.jsonlogger import JsonFormatter

from src.settings import settings


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["service_version"] = settings.SERVICE_VERSION
        log_record["worker_id"] = os.getpid()


def setup_json_logging() -> logging.Logger:
    common_handler = logging.StreamHandler()

    if settings.STAGE == "LOCAL":
        format_ = "%(levelname)s:%(name)s:%(asctime)s:%(message)s"
        datefmt = "%H:%M:%S"
        basic_formatter = logging.Formatter(format_, datefmt=datefmt)
        common_handler.setFormatter(basic_formatter)
    else:
        format_ = "%(timestamp)s %(levelname)s %(name)s %(message)s %(filename)s %(funcName)s %(lineno)s"
        json_formatter = CustomJsonFormatter(format_, timestamp=True)
        common_handler.setFormatter(json_formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(common_handler)
    root_logger.setLevel(logging.INFO)

    app_logger = logging.getLogger("src")
    app_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    logging.getLogger("uvicorn").handlers = [common_handler]
    logging.getLogger("uvicorn.error").handlers = [common_handler]
    logging.getLogger("uvicorn.access").handlers = [common_handler]

    return app_logger


app_logger = setup_json_logging()
