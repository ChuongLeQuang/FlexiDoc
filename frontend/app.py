"""
EN: Main entry point for the Streamlit Web Application.
VI: Điểm vào chính cho Ứng dụng Web Streamlit.
"""

import os
import sys
import base64
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

    # --- ĐÓNG DẤU BẢN QUYỀN TRÊN GIAO DIỆN ---
    st.sidebar.divider()

    # Nhúng Logo và chèn Tooltip bản quyền (hiển thị khi rê chuột)
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    logo_path = os.path.join(base_dir, "assets", "2CJ1.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()

        html_code = f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="data:image/png;base64,{encoded_img}" 
                 title="© 2026 Phần mềm độc quyền của tác giả Lê Quang Chương. Nghiêm cấm sao chép dưới mọi hình thức!" 
                 style="max-width: 70%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </div>
        """
        st.sidebar.markdown(html_code, unsafe_allow_html=True)

    st.sidebar.info(
        "**© 2026 Bản quyền thuộc về Lê Quang Chương**\n\n"
        "Phần mềm này được thiết kế và lập trình độc lập, dùng riêng cho nội bộ sử dụng.\n\n"
        "Nghiêm cấm sao chép, thương mại hóa hoặc nhận làm tài sản của tổ chức/nhà trường "
        "khi chưa có sự đồng ý bằng văn bản của Tác giả (Lê Quang Chương)."
    )


if __name__ == "__main__":
    main()
