"""
EN: Core service for rendering Word templates and packaging to ZIP.
VI: Dịch vụ lõi để trộn dữ liệu vào mẫu Word và nén thành file ZIP.
"""

import io
import zipfile
import jinja2
import decimal
from decimal import Decimal, ROUND_HALF_UP
from docxtpl import DocxTemplate, RichText
from typing import Dict, List, Any, Union

from src.utils.string_utils import sanitize_filename
from src.utils.number_to_words import number_to_words_vn
from src.services import word_service


def apply_formatting(value: str, format_type: str) -> Union[str, RichText]:
    """
    EN: Apply specific formats (currency, words, newlines) to the string.
    VI: Áp dụng định dạng (tiền tệ, chữ, xuống dòng) cho chuỗi dữ liệu.
    """
    if not value:
        return ""

    formatted_val = value

    # Xử lý định dạng theo yêu cầu
    if format_type == "currency":
        try:
            num_str = value.replace(",", "").replace(" ", "")
            # Sử dụng Decimal để làm tròn chuẩn (Round half up)
            num_dec = Decimal(num_str).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            formatted_val = f"{int(num_dec):,}".replace(",", ".")
        except (ValueError, decimal.InvalidOperation):
            formatted_val = value

    elif format_type == "number_to_words":
        try:
            num = float(value.replace(",", "").replace(" ", ""))
            formatted_val = number_to_words_vn(num)
        except ValueError:
            formatted_val = value

    # Xử lý xuống dòng (Multi-line / Alt+Enter trong Excel)
    if "\n" in formatted_val:
        rt = RichText()
        rt.add(formatted_val)
        return rt

    return formatted_val


def group_data_by_key(
    data: List[Dict[str, Any]], grouping_key: str = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    EN: Group rows of data by a specific key.
    VI: Gom nhóm các dòng dữ liệu dựa trên một cột khóa.
    """
    if not grouping_key:
        return {"default": data}

    grouped = {}
    for row in data:
        key_val = str(row.get(grouping_key, "")).strip()
        if not key_val:
            key_val = "Unknown"

        if key_val not in grouped:
            grouped[key_val] = []
        grouped[key_val].append(row)

    return grouped


def render_and_zip(
    template_bytes: bytes,
    grouped_data: Dict[str, List[Dict[str, Any]]],
    rules: List[Dict[str, Any]],
    filename_pattern: str,
) -> bytes:
    """
    EN: Render Word templates in memory and compress them into a ZIP archive.
    VI: Trộn dữ liệu vào Word trên bộ nhớ đệm và nén thành file ZIP.
    """
    zip_buffer = io.BytesIO()
    seen_filenames = set()
    jinja_env = jinja2.Environment()

    # Tiền xử lý mẫu Word (chuyển đổi table_start/table_end thành cú pháp Jinja2)
    processed_template_bytes = word_service.preprocess_template(template_bytes)

    # Tổng hợp rules để tránh query vòng lặp
    single_rules = [r for r in rules if r.get("variable_type") == "single"]
    table_rules = [r for r in rules if r.get("variable_type") == "table"]

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for group_key, rows in grouped_data.items():
            if not rows:
                continue

            context = {}
            first_row = rows[0]

            # 1. Gắn Biến Đơn (lấy từ dòng đầu tiên của nhóm)
            for r in single_rules:
                val = first_row.get(r["excel_col"], "")
                context[r["word_var"]] = apply_formatting(
                    val, r.get("format_type", "text")
                )

            # 2. Gắn Biến Bảng (gộp danh sách các dòng vào list)
            # Gom các biến bảng theo prefix (VD: ds.stt -> bảng 'ds', cột 'stt')
            table_contexts = {}
            for r in table_rules:
                var_parts = r["word_var"].split(".", 1)
                table_name = var_parts[0] if len(var_parts) > 1 else "table_data"
                field_name = var_parts[1] if len(var_parts) > 1 else r["word_var"]

                if table_name not in table_contexts:
                    table_contexts[table_name] = [{} for _ in range(len(rows))]

                for idx, row_data in enumerate(rows):
                    val = row_data.get(r["excel_col"], "")
                    table_contexts[table_name][idx][field_name] = apply_formatting(
                        val, r.get("format_type", "text")
                    )

            context.update(table_contexts)

            # 3. Đặt tên file (Có hỗ trợ Jinja2 từ biến context)
            try:
                name_tpl = jinja_env.from_string(filename_pattern or "Result_{{id}}")
                rendered_name = name_tpl.render(**context)
            except Exception:
                rendered_name = f"Result_{group_key}"

            safe_name = sanitize_filename(rendered_name)
            if not safe_name.endswith(".docx"):
                safe_name += ".docx"

            # 4. Chống ghi đè file (Name Collisions)
            base_name = safe_name[:-5]
            counter = 1
            final_name = safe_name
            while final_name in seen_filenames:
                final_name = f"{base_name}_{counter}.docx"
                counter += 1
            seen_filenames.add(final_name)

            # 5. Render và ghi vào ZIP
            tpl = DocxTemplate(io.BytesIO(processed_template_bytes))
            tpl.render(context)

            doc_buffer = io.BytesIO()
            tpl.save(doc_buffer)
            zip_file.writestr(final_name, doc_buffer.getvalue())

    return zip_buffer.getvalue()
