"""
EN: Unit tests for Generator Service.
VI: Kịch bản kiểm thử cho Dịch vụ Sinh tài liệu.
"""

from docxtpl import RichText
from src.services.generator_service import apply_formatting, group_data_by_key


def test_apply_formatting_currency():
    """Kiểm tra ép kiểu tiền tệ."""
    assert apply_formatting("1500000", "currency") == "1.500.000"
    assert apply_formatting("1500000.5", "currency") == "1.500.001"  # Làm tròn
    assert apply_formatting("NotANumber", "currency") == "NotANumber"


def test_apply_formatting_words():
    """Kiểm tra gọi hàm đổi số thành chữ."""
    assert apply_formatting("15000", "number_to_words") == "Mười lăm nghìn"


def test_apply_formatting_richtext():
    """Kiểm tra nhận diện xuống dòng tạo RichText."""
    result = apply_formatting("Dòng 1\nDòng 2", "text")
    assert isinstance(result, RichText)


def test_group_data_by_key():
    """Kiểm tra gom nhóm dòng dữ liệu."""
    data = [
        {"Phòng ban": "IT", "Tên": "Alice"},
        {"Phòng ban": "IT", "Tên": "Bob"},
        {"Phòng ban": "HR", "Tên": "Charlie"},
        {"Phòng ban": "", "Tên": "David"},
    ]

    # Test gom theo Phòng ban
    grouped = group_data_by_key(data, "Phòng ban")
    assert len(grouped["IT"]) == 2
    assert len(grouped["HR"]) == 1
    assert len(grouped["Unknown"]) == 1  # Nhóm rỗng tự động đưa vào Unknown

    # Test không có khóa gom nhóm (gom tất cả)
    default_grouped = group_data_by_key(data, None)
    assert len(default_grouped["default"]) == 4
