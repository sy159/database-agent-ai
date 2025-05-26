import sys
from loguru import logger
from typing import Literal, Optional
from pathlib import Path
from app.core.settings import settings
import os

LOG_FORMAT_TEXT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level}</level> | "
    "PID:{process} | TID:{thread} | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

LOG_FORMAT_JSON = (
    '{{'
    '"time": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
    '"level": "{level}", '
    '"process": "{process}", '
    '"thread": "{thread}", '
    '"file": "{name}", '
    '"function": "{function}", '
    '"line": {line}, '
    '"message": "{message}"'
    '}}'
)

_logger_registry = {}  # 防止重复添加 sink


def init_logger():
    logger.remove()
    cfg = settings.LOGGER
    fmt = LOG_FORMAT_JSON if cfg.format == "json" else LOG_FORMAT_TEXT

    def _add_file_sink(file_path: str):
        Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
        if cfg.rotation == "size":
            logger.add(file_path, rotation=cfg.max_bytes, retention=cfg.backup_count, format=fmt, enqueue=True)
        else:  # 默认按天切割：每天 00:00
            logger.add(file_path, rotation="00:00", retention=cfg.backup_count, format=fmt, enqueue=True)

    if cfg.output in ("console", "both"):
        logger.add(sys.stdout, format=fmt, enqueue=True)
    if cfg.output in ("file", "both"):
        _add_file_sink(cfg.file_name)


def get_logger(
        name: str,
        file_name: str,
        format_type: Literal["json", "text"] = "json",
        rotation: Literal["size", "time"] = "size",
        max_bytes: Optional[int] = 10 * 1024 * 1024,
        backup_count: int = 7,
) -> logger.__class__:
    if name in _logger_registry:
        return _logger_registry[name]

    sub_logger = logger.bind(name=name)
    sub_logger.remove()  # 清除默认配置
    fmt = LOG_FORMAT_JSON if format_type == "json" else LOG_FORMAT_TEXT
    Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)

    if rotation == "size":
        sub_logger.add(file_name, rotation=max_bytes, retention=backup_count, format=fmt, enqueue=True)
    else:
        sub_logger.add(file_name, rotation="00:00", retention=backup_count, format=fmt, enqueue=True)

    _logger_registry[name] = sub_logger
    return sub_logger
