from logging.handlers import RotatingFileHandler
import logging
import os

# TODO: maybe move this to config
LOG_FILE = "app.log"

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3  # 5MB per file, keeps 3 backups
)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

logging.basicConfig(level=log_level, handlers=[file_handler, console_handler])

logger = logging.getLogger("AutoMeet")