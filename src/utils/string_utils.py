"""
EN: String manipulation utilities.
VI: Các hàm tiện ích thao tác với chuỗi.
"""

import re


def sanitize_filename(name: str) -> str:
    """
    EN: Remove invalid characters from OS filename.
    VI: Loại bỏ các ký tự cấm của hệ điều hành trong tên file để tránh lỗi ZIP.
    """
    if not name:
        return "untitled"

    # Thay thế ký tự cấm \ / : * ? " < > | bằng dấu gạch dưới
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", name)

    # Xóa khoảng trắng thừa (multiple spaces) và strip 2 đầu
    sanitized = " ".join(sanitized.split())
    return sanitized.strip()
