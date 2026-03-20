"""
日志工具 - 基于 loguru
"""
import sys
import os
from loguru import logger

from common.config import Config

# 移除默认 handler
logger.remove()

# 控制台输出
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)

# 文件输出
log_dir = os.path.join(Config.PROJECT_ROOT, "logs")
os.makedirs(log_dir, exist_ok=True)

logger.add(
    os.path.join(log_dir, "{time:YYYY-MM-DD}.log"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {name}:{line} - {message}",
    level="DEBUG",
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
)
