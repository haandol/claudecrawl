import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_filename: Optional[str] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    console_handler = RichHandler(level=level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_filename:
        log_path = Path(log_filename).resolve().parent
        _ = log_path.exists() or log_path.mkdir(exist_ok=True, parents=True)

        file_handler = RotatingFileHandler(
            filename=log_filename,
            mode="a",
            maxBytes=2 * 1024 * 1024,  # 2MB
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"[{name}] Logging at {log_filename}...")

    return logger
