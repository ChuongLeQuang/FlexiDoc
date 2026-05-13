"""
EN: Unit tests for utility functions.
VI: Kiểm thử tự động cho các hàm tiện ích.
"""

import pytest
from src.utils.string_utils import sanitize_filename
from src.utils.number_to_words import number_to_words_vn


def test_sanitize_filename():
    """
    EN: Test filename sanitization logic.
    VI: Kiểm thử logic làm sạch tên file hệ điều hành.
    """
    # Kiểm tra loại bỏ ký tự cấm (Ví dụ A/B:C*D -> A_B_C_D)
    assert sanitize_filename("A/B:C*D") == "A_B_C_D"

    # Kiểm tra loại bỏ khoảng trắng thừa
    assert sanitize_filename("   File   Test  .docx  ") == "File Test .docx"

    # Kiểm tra chuỗi rỗng
    assert sanitize_filename("") == "untitled"
    assert sanitize_filename(None) == "untitled"


def test_number_to_words_vn():
    """
    EN: Test converting numbers to Vietnamese words.
    VI: Kiểm thử logic đổi số thành chữ tiếng Việt.
    """
    # Kiểm tra các số tròn
    assert number_to_words_vn(15000) == "Mười lăm nghìn"
    assert number_to_words_vn(0) == "Không"

    # Kiểm tra số âm
    assert number_to_words_vn(-50) == "Âm năm mươi"

    # Kiểm tra số phức tạp
    assert number_to_words_vn(105) == "Một trăm lẻ năm"
    assert (
        number_to_words_vn(1234567)
        == "Một triệu hai trăm ba mươi tư nghìn năm trăm sáu mươi bảy"
    )
