"""
EN: UI Component for the Tag Builder Assistant (Popup).
VI: Thành phần giao diện cho Module Trợ lý Sinh Thẻ & Tạo Excel (Popup).
"""

import streamlit as st
import frontend.api_client as api_client
import unicodedata
import re
import json


def create_var_name(text: str) -> str:
    """Loại bỏ dấu, ký tự đặc biệt và tạo tên biến dạng snake_case."""
    text = text.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    s = re.sub(r"[^a-zA-Z0-9\s]", "", s).strip()
    s = re.sub(r"\s+", "_", s).lower()
    return s


@st.dialog("✨ Trợ lý Sinh Thẻ & Tạo Excel", width="large")
def render_assistant_modal():
    st.write(
        "Khai báo các thông tin bạn cần điền vào Hợp đồng/Biểu mẫu để hệ thống tạo Thẻ (Tags) chuẩn xác."
    )

    if "tags_single" not in st.session_state:
        st.session_state.tags_single = []
    if "tags_table" not in st.session_state:
        st.session_state.tags_table = []

    with st.expander("💾 Lưu / Khôi phục Bản nháp (Tùy chọn)"):
        st.markdown(
            "Sử dụng tính năng này nếu bạn đang tạo nhiều biến và muốn lưu lại để đề phòng mất dữ liệu."
        )
        col_in, col_out = st.columns(2)

        with col_in:
            uploaded_json = st.file_uploader(
                "📥 Tải lên bản nháp (.json)", type=["json"], key="draft_uploader"
            )
            if uploaded_json and st.button(
                "🔄 Khôi phục dữ liệu", use_container_width=True
            ):
                try:
                    data = json.load(uploaded_json)
                    st.session_state.tags_single = data.get("tags_single", [])
                    st.session_state.tags_table = data.get("tags_table", [])
                    st.success("Đã khôi phục thành công!")
                    st.rerun()
                except Exception:
                    st.error("File nháp không hợp lệ.")

        with col_out:
            st.write("")
            st.write("")
            draft_data = {
                "tags_single": st.session_state.tags_single,
                "tags_table": st.session_state.tags_table,
            }
            draft_json = json.dumps(draft_data, ensure_ascii=False, indent=4).encode(
                "utf-8"
            )
            st.download_button(
                "💾 Tải file Bản Nháp (.json)",
                data=draft_json,
                file_name="FlexiDoc_Draft.json",
                mime="application/json",
                key="download_draft_btn",
                use_container_width=True,
                help="Lưu ý: Tệp sẽ được tải qua trình duyệt. Nếu không thấy hộp thoại lưu, hãy kiểm tra thư mục 'Downloads' của máy tính.",
            )

    tab1, tab2 = st.tabs(["🏷️ Biến đơn", "📋 Bảng/Danh sách lặp"])

    with tab1:
        st.markdown(
            "**Biến đơn** dùng cho các thông tin đứng một mình (Ví dụ: Họ tên, Số hợp đồng...)."
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            single_input = st.text_input(
                "Tên thông tin cần điền",
                placeholder="VD: Tên nhân viên",
                key="single_input",
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("➕ Thêm biến"):
                if single_input:
                    var_name = create_var_name(single_input)
                    if var_name and var_name not in st.session_state.tags_single:
                        st.session_state.tags_single.append(var_name)
                    st.rerun()

    with tab2:
        st.markdown(
            "**Bảng/Danh sách lặp** dùng cho các thông tin lặp lại nhiều dòng (Ví dụ: Danh sách thiết bị, Danh sách lớp học...)."
        )
        t_col0, t_col1, t_col2, t_col3 = st.columns([2, 2, 2, 1])
        with t_col0:
            table_type_input = st.selectbox(
                "Kiểu lặp", ["Bảng (Table)", "Danh sách (List)"], key="table_type_input"
            )
        with t_col1:
            table_name_input = st.text_input(
                "Tên Bảng/Danh sách",
                placeholder="VD: Danh sách lớp",
                key="table_name_input",
            )
        with t_col2:
            table_col_input = st.text_input(
                "Tên Cột/Thông tin lặp",
                placeholder="VD: Tên môn học",
                key="table_col_input",
            )
        with t_col3:
            st.write("")
            st.write("")
            if st.button("➕ Thêm cột"):
                if table_name_input and table_col_input:
                    t_name = create_var_name(table_name_input)
                    c_name = create_var_name(table_col_input)
                    if t_name and c_name:
                        found = False
                        for t in st.session_state.tags_table:
                            if t["name"] == t_name:
                                if c_name not in t["cols"]:
                                    t["cols"].append(c_name)
                                t["type"] = (
                                    "table" if "Bảng" in table_type_input else "list"
                                )
                                found = True
                                break
                        if not found:
                            st.session_state.tags_table.append(
                                {
                                    "name": t_name,
                                    "type": (
                                        "table"
                                        if "Bảng" in table_type_input
                                        else "list"
                                    ),
                                    "cols": [c_name],
                                }
                            )
                    st.rerun()

    st.divider()
    st.subheader("📋 Thẻ của bạn (Rê chuột vào góc phải thẻ để Copy)")

    if not st.session_state.tags_single and not st.session_state.tags_table:
        st.info(
            "Hãy thêm biến ở phía trên, các thẻ sẽ xuất hiện ở đây để bạn Copy dán vào file Word."
        )

    # Render Biến đơn
    for idx, var in enumerate(st.session_state.tags_single):
        c1, c2, c3 = st.columns([1, 4, 1])
        c1.markdown(f"**Biến đơn:**")
        c2.code(f"{{{{ {var} }}}}")
        if c3.button("❌ Xóa", key=f"del_s_{idx}"):
            st.session_state.tags_single.pop(idx)
            st.rerun()

    # Render Biến Bảng
    for t_idx, table in enumerate(st.session_state.tags_table):
        t_type = table.get("type", "table")
        t_label = "Bảng" if t_type == "table" else "Danh sách"
        t_start = (
            f"table_start:{table['name']}"
            if t_type == "table"
            else f"list_start:{table['name']}"
        )
        t_end = "table_end" if t_type == "table" else "list_end"

        st.markdown(f"**{t_label}: {table['name']}**")
        c1, c2 = st.columns([5, 1])
        c1.code(f"{{{{ {t_start} }}}}")
        if c2.button("❌ Xóa nhóm", key=f"del_t_{t_idx}"):
            st.session_state.tags_table.pop(t_idx)
            st.rerun()

        for c_idx, col in enumerate(table["cols"]):
            c1, c2, c3 = st.columns([1, 4, 1])
            c1.markdown(f"- *Biến lặp:*")
            c2.code(f"{{{{ item.{col} }}}}")
            if c3.button("❌ Xóa", key=f"del_tc_{t_idx}_{c_idx}"):
                table["cols"].pop(c_idx)
                st.rerun()

        st.code(f"{{{{ {t_end} }}}}")

    st.divider()
    if st.button(
        "📥 Tải file Excel Nhập liệu", type="primary", use_container_width=True
    ):
        if not st.session_state.tags_single and not st.session_state.tags_table:
            st.warning("Bạn chưa tạo biến nào!")
        else:
            with st.spinner("Đang tạo Excel..."):
                try:
                    excel_vars = []
                    excel_vars.extend(st.session_state.tags_single)
                    if st.session_state.tags_table:
                        excel_vars.insert(0, "Mã Khóa (VD: Ma_NV)")
                    for table in st.session_state.tags_table:
                        excel_vars.extend(table["cols"])

                    excel_bytes = api_client.assistant_generate_excel(excel_vars)
                    st.session_state.generated_excel = excel_bytes
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    if st.session_state.get("generated_excel"):
        st.success("Tạo thành công! Hãy tải file Excel về để nhập dữ liệu.")
        st.download_button(
            label="⬇️ Tải file Du_Lieu_Mau.xlsx",
            data=st.session_state.generated_excel,
            file_name="Du_Lieu_Mau.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )

    st.divider()
    if st.button("Đóng Trợ lý"):
        st.session_state.show_assistant = False
        st.rerun()
