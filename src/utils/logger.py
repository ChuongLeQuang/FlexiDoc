"""
EN: Application logger configuration.
VI: Cấu hình hệ thống ghi log của ứng dụng.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Đảm bảo thư mục logs được tạo ở ngoài root của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "flexidoc.log")


def get_logger(name: str) -> logging.Logger:
    """Khởi tạo và trả về đối tượng logger."""
    logger = logging.getLogger(name)

    # Nếu logger đã được cấu hình trước đó, trả về luôn để tránh log bị lặp nhiều dòng
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Cấu hình log ra file (Xoay vòng file khi đạt 5MB, giữ lại 3 file cũ)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    # Cấu hình in log trực tiếp ra cửa sổ console (Terminal)
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
