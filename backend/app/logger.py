import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import date

LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        # Console handler — keeps logs visible in `docker compose logs`
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # File handler — rotates daily, keeps 30 days of logs
        file_handler = TimedRotatingFileHandler(
            LOG_DIR / f"{date.today()}.log",
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y-%m-%d"

        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger