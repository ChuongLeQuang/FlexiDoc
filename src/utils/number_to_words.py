"""
EN: Utility to convert numbers to Vietnamese words.
VI: Tiện ích chuyển đổi số thành chữ tiếng Việt.
"""

import math


def _read_group(group: int, full: bool = False) -> str:
    """Hàm phụ trợ để đọc một cụm 3 chữ số."""
    digits = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    hundred = group // 100
    ten = (group % 100) // 10
    unit = group % 10
    res = ""

    if full or hundred > 0:
        res += digits[hundred] + " trăm "

    if ten == 0 and unit > 0 and (full or hundred > 0):
        res += "lẻ "
    elif ten == 1:
        res += "mười "
    elif ten > 1:
        res += digits[ten] + " mươi "

    if ten > 1 and unit == 1:
        res += "mốt"
    elif ten > 1 and unit == 4:
        res += "tư"
    elif ten > 0 and unit == 5:
        res += "lăm"
    elif unit > 0:
        res += digits[unit]

    return res.strip()


def number_to_words_vn(number: float) -> str:
    """
    EN: Convert a number to Vietnamese text.
    VI: Chuyển đổi số thành chữ tiếng Việt (hỗ trợ đến hàng tỷ).
    """
    if number == 0:
        return "Không"

    is_negative = number < 0
    number = abs(math.floor(number))
    if number == 0:
        return "Không"

    units = ["", "nghìn", "triệu", "tỷ"]
    parts = []
    while number > 0:
        parts.append(number % 1000)
        number //= 1000

    res = [
        _read_group(part, full=(i < len(parts) - 1)) + f" {units[i]}"
        for i, part in enumerate(parts)
        if part > 0 or (i == len(parts) - 1 and part == 0)
    ]
    final_str = " ".join(reversed(res)).strip()
    if is_negative:
        final_str = f"âm {final_str}"
    return final_str.capitalize()
