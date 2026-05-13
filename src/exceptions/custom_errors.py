"""
EN: Custom exception classes for specific business logic errors.
VI: Các lớp ngoại lệ tự định nghĩa cho lỗi nghiệp vụ cụ thể.
"""


class FlexiDocBaseError(Exception):
    """Lớp cơ sở cho các lỗi của FlexiDoc."""

    pass


class InvalidFileFormatError(FlexiDocBaseError):
    """Lỗi khi định dạng file (Word/Excel) tải lên không hợp lệ hoặc bị hỏng."""

    pass


class TemplateSyntaxError(FlexiDocBaseError):
    """Lỗi cú pháp thẻ biến Jinja2 trong mẫu Word."""

    pass


class ZeroVariableError(FlexiDocBaseError):
    """Lỗi khi file Word không chứa bất kỳ thẻ ngoặc nhọn nào ({{...}})."""

    pass


class SheetNotFoundError(FlexiDocBaseError):
    """Lỗi khi không tìm thấy tên Sheet được cấu hình trong file Excel."""

    pass


class EmptyHeaderRowError(FlexiDocBaseError):
    """Lỗi khi dòng tiêu đề (Header row) của Excel hoàn toàn trống."""

    pass
