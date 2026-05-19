"""
EN: UI Component for handling file uploads and triggering validation.
VI: Thành phần giao diện xử lý tải tệp lên và kích hoạt kiểm tra lỗi.
"""

import streamlit as st
import time
import io
from typing import Dict, Optional, Any
import frontend.api_client as api_client
from frontend.components.assistant_modal import render_assistant_modal


def render_onboarding_ui() -> None:
    """
    EN: Render onboarding instructions for 0-variable Word templates.
    VI: Hiển thị hướng dẫn nhúng biến cho mẫu Word không có biến nào.
    """
    st.warning(
        "💡 **Hệ thống không tìm thấy biến dữ liệu nào trong file Word của bạn.**"
    )

    if st.button(
        "✨ Mở Trợ lý Đục lỗ",
        type="primary",
        use_container_width=True,
        key="open_assistant",
    ):
        st.session_state.show_assistant = True
        st.rerun()

    st.markdown("""
        ### 📖 Hoặc làm thủ công theo các bước sau:
        1. Mở file Word của bạn lên.
        2. Thay thế những chỗ cần điền tự động bằng cặp dấu ngoặc nhọn. 
           *Ví dụ: Thay chữ `Nguyễn Văn A` thành `{{ ho_ten }}`.*
        3. Nếu có bảng biểu, hãy bọc dòng cần lặp bằng `{{table_start:ten_danh_sach}}` và `{{table_end}}`.
        4. Lưu file Word lại và tải lên hệ thống một lần nữa.
        """)


def handle_file_upload() -> Optional[Dict[str, Any]]:
    """
    EN: Render file uploaders and handle validation flow.
    VI: Hiển thị khu vực tải file và xử lý luồng kiểm tra lỗi.
    """
    # Gọi hiển thị popup nếu cờ đang được bật
    if st.session_state.get("show_assistant"):
        render_assistant_modal()

    # Hiển thị nút gọi Trợ lý trực tiếp ở màn hình chính
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.info(
            "💡 **Lần đầu sử dụng?** Nếu file Word của bạn là file tĩnh (chưa đục lỗ) và chưa có file Excel, hãy mở Trợ lý."
        )
    with col_btn:
        if st.button(
            "✨ Mở Trợ lý",
            type="primary",
            use_container_width=True,
            key="open_assistant_main",
        ):
            st.session_state.show_assistant = True
            st.rerun()

    st.write(
        "Vui lòng tải lên **cả file Mẫu Word và file Dữ liệu Excel** để hệ thống có thể đọc trên bộ nhớ đệm (Zero-Disk)."
    )

    col1, col2 = st.columns(2)
    with col1:
        docx_file = st.file_uploader("📄 Tải lên Mẫu Word (.docx)", type=["docx"])
    with col2:
        xlsx_file = st.file_uploader("📊 Tải lên Dữ liệu Excel (.xlsx)", type=["xlsx"])

    # Tự động đọc danh sách Sheet từ file Excel
    sheet_names = ["Sheet1"]
    if xlsx_file:
        try:
            import openpyxl

            wb = openpyxl.load_workbook(
                io.BytesIO(xlsx_file.getvalue()), read_only=True, data_only=True
            )
            sheet_names = wb.sheetnames
            wb.close()
        except Exception:
            pass

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        sheet_name = st.selectbox("Tên Sheet dữ liệu", sheet_names)
    with col4:
        header_row = st.number_input("Dòng chứa Tiêu đề", min_value=1, value=1)

    if st.button(
        "🔍 Kiểm tra & Phân tích Dữ liệu", type="primary", use_container_width=True
    ):
        if not docx_file or not xlsx_file:
            st.error(
                "⚠️ Vui lòng tải lên đầy đủ cả file Word và file Excel trước khi kiểm tra."
            )
            return None

        with st.spinner("Đang phân tích cấu trúc file Word và Excel..."):
            response = api_client.validate_templates(
                docx_file, xlsx_file, sheet_name, header_row
            )

        if response["status"] == "error":
            error_code = response.get("error_code")
            if error_code == "ZERO_VARIABLES":
                render_onboarding_ui()
            else:
                st.error(f"❌ **Lỗi ({error_code})**: {response.get('message')}")
                if response.get("details"):
                    st.json(response.get("details"))
            return None
        else:
            st.success(
                "✅ Phân tích thành công! Mời bạn tiếp tục cấu hình Mapping bên dưới."
            )
            data = response["data"]
            data["docx_bytes"] = docx_file.getvalue()
            data["xlsx_bytes"] = xlsx_file.getvalue()
            data["docx_name"] = docx_file.name
            data["xlsx_name"] = xlsx_file.name
            data["sheet_name"] = sheet_name
            data["header_row"] = header_row
            return data

    return None
