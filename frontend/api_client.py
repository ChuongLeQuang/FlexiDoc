"""
EN: API Client to handle communication between Streamlit UI and FastAPI Backend.
VI: API Client để xử lý giao tiếp giữa giao diện Streamlit và Backend FastAPI.
"""

import requests
import json
from typing import Dict, Any, List

BASE_URL = "http://127.0.0.1:8000/api/v1"


def validate_templates(
    docx_file: Any, xlsx_file: Any, sheet_name: str = "Sheet1", header_row: int = 1
) -> Dict[str, Any]:
    """
    EN: Call API to validate uploaded templates.
    VI: Gọi API để kiểm tra các tệp mẫu đã tải lên.
    """
    # Validate Word
    word_res = requests.post(
        f"{BASE_URL}/templates/validate",
        files={
            "file": (
                docx_file.name,
                docx_file.getvalue(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    if word_res.status_code != 200:
        return {"status": "error", **word_res.json()}

    word_data = word_res.json()
    flat_word_vars = word_data.get("single_vars", [])
    for table_name, vars_list in word_data.get("table_vars", {}).items():
        for v in vars_list:
            flat_word_vars.append(f"{table_name}.{v}")

    # Validate Excel
    excel_res = requests.post(
        f"{BASE_URL}/excel/validate",
        files={
            "file": (
                xlsx_file.name,
                xlsx_file.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
        data={"sheet_name": sheet_name, "header_row": header_row},
    )

    if excel_res.status_code != 200:
        return {"status": "error", **excel_res.json()}

    excel_data = excel_res.json()

    return {
        "status": "success",
        "data": {
            "message": "Dữ liệu hợp lệ để Mapping",
            "word_vars": flat_word_vars,
            "excel_cols": excel_data.get("columns", []),
            "sheet_names": excel_data.get("sheet_names", []),
        },
    }


def get_format_types() -> List[str]:
    """
    EN: Fetch available formatting types.
    VI: Lấy danh sách các loại định dạng được hỗ trợ.
    """
    return ["text", "date", "currency", "number_to_words"]


def generate_document(payload: Dict[str, Any]) -> bytes:
    """
    EN: Call API to generate and ZIP documents.
    VI: Gọi API để sinh và nén tài liệu.
    """
    mapping_config = payload["mapping_config"]
    upload_data = payload["upload_data"]

    files = {
        "word_file": (
            upload_data["docx_name"],
            upload_data["docx_bytes"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "excel_file": (
            upload_data["xlsx_name"],
            upload_data["xlsx_bytes"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
    }

    data = {
        "sheet_name": upload_data.get("sheet_name", "Sheet1"),
        "header_row": upload_data.get("header_row", 1),
        "grouping_key": (
            mapping_config.get("grouping_key", "")
            if mapping_config.get("grouping_key")
            else ""
        ),
        "filename_pattern": mapping_config.get("filename_pattern", "Result_{{id}}"),
        "rules": json.dumps(mapping_config.get("rules", [])),
        "filter_col": mapping_config.get("filter_col", ""),
        "selected_keys": json.dumps(mapping_config.get("selected_keys", [])),
    }

    res = requests.post(f"{BASE_URL}/documents/generate", files=files, data=data)

    if res.status_code == 200:
        return res.content
    else:
        error_msg = (
            res.json().get("message", res.text)
            if "application/json" in res.headers.get("content-type", "")
            else res.text
        )
        raise Exception(f"Lỗi từ server: {error_msg}")


def assistant_generate_excel(variables: List[str]) -> bytes:
    """
    EN: Call API to generate Excel template.
    VI: Gọi API để sinh file Excel mẫu.
    """
    res = requests.post(f"{BASE_URL}/assistant/generate-excel", json=variables)
    if res.status_code == 200:
        return res.content
    raise Exception(f"Lỗi tạo file mẫu: {res.text}")
