import logging
import logging.config
from datetime import datetime
from zoneinfo import ZoneInfo

_BERLIN_TZ = ZoneInfo("Europe/Berlin")


class _BerlinFormatter(logging.Formatter):
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        dt = datetime.fromtimestamp(record.created, tz=_BERLIN_TZ)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def configure_logging(level: str = "INFO") -> None:
    formatter = _BerlinFormatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
