"""
EN: UI Component for mapping Excel columns to Word variables.
VI: Thành phần giao diện để ánh xạ cột Excel với biến Word.
"""

import streamlit as st
from typing import List, Dict, Any
import frontend.api_client as api_client
import unicodedata
import re


def _normalize_string(s: str) -> str:
    """Loại bỏ dấu tiếng Việt và ký tự đặc biệt để so sánh chuỗi."""
    s = unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _guess_col_index(word_var: str, excel_cols: List[str]) -> int:
    """Đoán cột Excel phù hợp nhất với biến Word."""
    if not excel_cols:
        return 0

    # Bỏ qua tiền tố của biến bảng (VD: ds.ten_thiet_bi -> ten_thiet_bi)
    var_clean = word_var.split(".")[-1]
    norm_var = _normalize_string(var_clean)

    # 1. So sánh khớp hoàn toàn
    for i, col in enumerate(excel_cols):
        if norm_var == _normalize_string(col):
            return i

    # 2. So sánh chứa (Substring match) - Dùng khi cột là "Họ tên nhân viên" còn biến là "hoten"
    for i, col in enumerate(excel_cols):
        norm_col = _normalize_string(col)
        if (
            len(norm_var) > 2
            and len(norm_col) > 2
            and (norm_var in norm_col or norm_col in norm_var)
        ):
            return i

    return 0


def render_mapping_rules(upload_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    EN: Render mapping UI with dynamic data from API client.
    VI: Hiển thị giao diện Mapping với dữ liệu động từ API client.
    """
    st.write(
        "Vui lòng ghép cặp các biến trong file Word với các cột tương ứng trong file Excel."
    )

    # Lấy dữ liệu động từ payload được truyền qua
    word_vars = upload_data.get("word_vars", []) if upload_data else []
    excel_cols = upload_data.get("excel_cols", []) if upload_data else []
    format_types = api_client.get_format_types()

    rules = []

    for var in word_vars:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.text_input(
                "Biến Word", value=f"{{{{ {var} }}}}", disabled=True, key=f"label_{var}"
            )
        with col2:
            default_idx = _guess_col_index(var, excel_cols)
            selected_col = st.selectbox(
                f"Cột Excel cho '{var}'",
                excel_cols,
                index=default_idx,
                key=f"col_{var}",
            )
        with col3:
            selected_fmt = st.selectbox(f"Định dạng", format_types, key=f"fmt_{var}")

        rules.append(
            {
                "variable_type": "table" if "." in var else "single",
                "word_var": var,
                "excel_col": selected_col,
                "format_type": selected_fmt,
            }
        )

    st.divider()
    st.subheader("⚙️ Cấu hình Gom nhóm & Đầu ra")

    with st.expander("💡 Khóa gom nhóm là gì? (Bấm để xem ví dụ minh họa)"):
        st.markdown("""
            **Khóa gom nhóm (Grouping Key)** giúp phần mềm biết cách gộp nhiều dòng dữ liệu trong Excel vào chung một file Word.
            
            *Ví dụ: Trong file Excel, nhân viên **Nguyễn Văn A** chiếm 2 dòng dữ liệu (được cấp 2 thiết bị).*
            - ✅ **Nếu chọn Khóa gom nhóm (Ví dụ chọn cột: Mã NV):** Hệ thống sẽ gom 2 dòng đó lại và tạo ra **1 file Hợp đồng riêng** cho anh A, bên trong bảng liệt kê đủ 2 thiết bị.
            - ❌ **Nếu KHÔNG chọn (Để trống):** Hệ thống sẽ gộp danh sách thiết bị của **tất cả mọi người trong công ty** và nhồi chung vào **1 tờ Hợp đồng duy nhất**.
            """)

    # Kiểm tra xem có biến bảng biểu không để ép buộc và tự động đoán khóa gom nhóm
    has_table_vars = any(r["variable_type"] == "table" for r in rules)

    if has_table_vars:
        st.warning(
            "⚠️ **Mẫu Word có Bảng biểu:** Bạn bắt buộc phải chọn Cột khóa gom nhóm (VD: Mã NV) để phần mềm biết cách tách các người khác nhau ra từng file riêng biệt."
        )
        default_grp_idx = 0
        # Tự động tìm các cột có chữ 'mã' hoặc 'id' để chọn sẵn
        for i, col in enumerate(excel_cols):
            norm = _normalize_string(col)
            if "ma" in norm or "id" in norm:
                default_grp_idx = i
                break
        grouping_key = st.selectbox(
            "🔑 Cột khóa gom nhóm:", excel_cols, index=default_grp_idx
        )
    else:
        grouping_key = st.selectbox(
            "🔑 Cột khóa gom nhóm (Tuỳ chọn):", [""] + excel_cols
        )

    filename_pattern = st.text_input(
        "Quy tắc đặt tên file Word",
        value="PhuLuc_{{ ho_ten }}",
        help="Ví dụ: PhuLuc_{{ho_ten}} hệ thống sẽ tạo ra file PhuLuc_NguyenVanA.docx",
    )

    return {
        "rules": rules,
        "filename_pattern": filename_pattern,
        "grouping_key": grouping_key,
    }
