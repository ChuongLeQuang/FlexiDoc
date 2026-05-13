"""
EN: Main entry point for the Streamlit Web Application.
VI: Điểm vào chính cho Ứng dụng Web Streamlit.
"""

import streamlit as st
from frontend.components.upload_section import handle_file_upload
from frontend.components.mapping_ui import render_mapping_rules
from frontend.components.generate_ui import handle_generation
from frontend.components.guide_tab import render_guide_tab


def init_session_state() -> None:
    """Khởi tạo các biến trạng thái cần thiết cho phiên làm việc."""
    if "upload_data" not in st.session_state:
        st.session_state.upload_data = None
    if "mapping_rules" not in st.session_state:
        st.session_state.mapping_rules = None


def main() -> None:
    """
    EN: Main function to configure and render the Streamlit UI.
    VI: Hàm chính để cấu hình và hiển thị giao diện Streamlit.
    """
    st.set_page_config(
        page_title="FlexiDoc - Auto Document Generator",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    st.title("📄 FlexiDoc")
    st.markdown(
        "**EN**: Automated Document Generation Platform<br>"
        "**VI**: Nền tảng Tự động hóa Khởi tạo Tài liệu",
        unsafe_allow_html=True,
    )
    st.divider()

    tab_run, tab_guide = st.tabs(["⚡ Chạy hệ thống", "📖 Hướng dẫn"])

    with tab_run:
        st.header("1. Tải lên dữ liệu (Upload)")
        new_upload_data = handle_file_upload()
        if new_upload_data:
            st.session_state.upload_data = new_upload_data

        st.header("2. Cấu hình Ánh xạ (Mapping)")
        if st.session_state.upload_data:
            st.session_state.mapping_rules = render_mapping_rules(
                st.session_state.upload_data
            )
        else:
            st.warning(
                "🔒 Vui lòng hoàn thành kiểm tra file ở Bước 1 để hiển thị Bảng cấu hình Mapping."
            )

        st.header("3. Sinh tài liệu (Generate)")
        if st.session_state.mapping_rules and st.session_state.upload_data:
            handle_generation(
                st.session_state.mapping_rules, st.session_state.upload_data
            )
        else:
            st.warning(
                "🔒 Vui lòng hoàn thành cấu hình ở Bước 2 để có thể tạo tài liệu."
            )

    with tab_guide:
        render_guide_tab()


if __name__ == "__main__":
    main()
