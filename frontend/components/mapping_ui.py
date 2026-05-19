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

    with st.expander("💡 Phân biệt bản chất: Sinh tài liệu vs Khóa gom nhóm"):
        st.markdown("""
            **1. Sinh tài liệu hàng loạt (Mặc định): Cơ chế 1-1**
            - Nguyên tắc: **Mỗi 1 dòng** trong file Excel sẽ sinh ra **1 file Word** độc lập.
            - *Ví dụ:* File Excel có 100 nhân viên -> Hệ thống tự động đẻ ra 100 tờ Hợp đồng riêng biệt.
            
            **2. Khóa Gom nhóm (Chỉ dùng khi Word có Bảng biểu): Cơ chế Nhiều-1**
            - Nguyên tắc: Gom **Nhiều dòng** trong Excel vào chung **1 cái bảng trong 1 file Word**.
            - *Ví dụ:* Anh Nguyễn Văn A mượn 3 thiết bị (nên tên anh A bị lặp lại ở 3 dòng trong Excel).
              👉 **Nếu CHỌN khóa (Ví dụ chọn cột: Mã NV):** Máy tính sẽ gom 3 dòng đó lại, nhét vào chung 1 cái Bảng trong 1 tờ Biên bản duy nhất của anh A.
              👉 **Nếu KHÔNG chọn khóa:** Máy tính sẽ áp dụng cơ chế 1-1 ở trên (In ra 3 tờ Biên bản rời rạc cho anh A, mỗi tờ chỉ ghi 1 cái thiết bị).
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

    st.divider()
    st.subheader("📄 Quy tắc đặt tên file đầu ra")

    single_vars = [v for v in word_vars if "." not in v]

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        file_prefix = st.text_input(
            "Tiền tố tên file",
            value="PhuLuc_",
            help="Đoạn chữ cố định ở đầu tên file (Ví dụ: PhuLuc_).",
            key="file_prefix_input",
        )
    with f_col2:
        file_var = st.selectbox(
            "Biến phân biệt",
            options=["(Không dùng biến)"] + single_vars,
            key="file_var_select",
            help="Chọn một biến (Ví dụ: ho_ten) để tự động ghép vào tên file, giúp các file không bị trùng nhau.",
        )

    if file_var != "(Không dùng biến)":
        filename_pattern = f"{file_prefix}{{{{ {file_var} }}}}"
    else:
        filename_pattern = file_prefix

    return {
        "rules": rules,
        "filename_pattern": filename_pattern,
        "grouping_key": grouping_key,
    }
