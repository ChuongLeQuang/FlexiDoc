"""
EN: UI Component for displaying User Guide.
VI: Thành phần giao diện hiển thị Hướng dẫn sử dụng.
"""

import streamlit as st


def render_guide_tab() -> None:
    """Hiển thị nội dung hướng dẫn người dùng."""
    st.header("📖 Hướng dẫn sử dụng FlexiDoc")
    st.markdown(
        "Chào mừng bạn đến với **FlexiDoc**! Nền tảng giúp bạn tự động hóa việc điền dữ liệu từ Excel vào các biểu mẫu Word. Dưới đây là hướng dẫn chi tiết:"
    )

    with st.expander(
        "📝 1. Cách chuẩn bị File Word (Mẫu Hợp đồng / Phụ lục)", expanded=True
    ):
        st.markdown("""
            ### A. Yêu cầu cơ bản (Điều kiện cần & đủ)
            - **Định dạng file:** Bắt buộc phải là file Word định dạng mới **`.docx`** (Hệ thống không hỗ trợ file `.doc` cũ hoặc `.pdf`).
            - **Nội dung:** Là một biểu mẫu, hợp đồng hoặc phụ lục chứa sẵn các văn bản cố định (quốc hiệu, tiêu ngữ, các điều khoản chung...).
            - **Nguyên tắc:** Những chỗ nào cần phần mềm tự động điền thông tin (như Họ tên, Ngày sinh, Số tiền...), bạn sẽ chèn các **"Biến"** vào đó theo hướng dẫn bên dưới.

            ### B. Chèn biến đơn giản
            Sử dụng cặp dấu ngoặc nhọn `{{ }}` để đánh dấu vị trí cần điền dữ liệu.
            *Ví dụ minh họa trong file Word:*
            > Hôm nay, ngày 01/01/2026, chúng tôi ký hợp đồng với ông/bà: **`{{ ho_ten }}`**
            > Sinh ngày: **`{{ ngay_sinh }}`**
            > Mức lương: **`{{ muc_luong }}`** VNĐ
            
            ### C. Chèn Bảng biểu động (Danh sách)
            Để tạo một bảng tự động thêm nhiều dòng (dựa trên dữ liệu Excel), bạn làm theo 3 bước:
            1. Tạo một dòng riêng ngay phía trên dòng dữ liệu, ghi **`{{ table_start:ten_bang }}`** vào ô đầu tiên.
               👉 *(**Lưu ý cực kỳ quan trọng:** `ten_bang` là một cái tên **do bạn tự nghĩ ra và đặt tùy ý** để dễ nhớ. Vui lòng viết liền, không dấu, không khoảng trắng. Ví dụ: bạn có thể tự đặt là `ds_thiet_bi`, `bang_luong`...)*
            2. Tạo một dòng riêng ngay phía dưới dòng dữ liệu, ghi **`{{ table_end }}`** vào ô đầu tiên.
            3. Các biến bên trong bảng bắt buộc phải có chữ **`item.`** ở trước (đại diện cho từng dòng dữ liệu). Ví dụ: `{{ item.ten_thiet_bi }}`.
            
            *Ví dụ minh họa Bảng trong Word:*
            | STT | Tên Thiết Bị | Số Lượng |
            |---|---|---|
            | `{{ table_start:ds_thiet_bi }}` | | |
            | `{{ item.stt }}` | `{{ item.ten_thiet_bi }}` | `{{ item.so_luong }}` |
            | `{{ table_end }}` | | |
            """)

    with st.expander("📊 2. Cách chuẩn bị File Excel (Dữ liệu)"):
        st.markdown("""
            ### A. Yêu cầu cơ bản (Điều kiện cần & đủ)
            - **Định dạng file:** Bắt buộc là file Excel định dạng mới **`.xlsx`**.
            - **Dòng Tiêu đề (Header):** Phải có một dòng chứa tên các cột rõ ràng (thường nằm ở dòng số 1). Hệ thống sẽ dùng dòng này để làm danh sách lựa chọn cho bạn.
            - **Nguyên tắc:** KHÔNG được gộp ô (Merge cells) ở dòng Tiêu đề. Tên các cột tuyệt đối không được trùng lặp nhau.
            
            ### B. Điều kiện liên kết với file Word (Cực kỳ quan trọng)
            Nhiều người thắc mắc: *"Làm sao để chữ trong Excel chạy được đúng vào chỗ trống trong Word?"*
            - **Không cần đặt tên giống nhau:** Tên cột trong Excel **không bắt buộc** phải gõ giống hệt tên Biến trong Word (Ví dụ: Word ghi biến `{{ ho_ten }}`, nhưng cột Excel ghi là `Họ và tên nhân viên` thì vẫn hoàn toàn hợp lệ).
            - **Sự liên kết (Ánh xạ):** Cầu nối giữa 2 file chính là **Giao diện Web (Bước 2)**. Hệ thống sẽ liệt kê các Biến Word, việc của bạn chỉ là click chọn Cột Excel tương ứng. Máy tính sẽ tự hiểu và đắp dữ liệu sang.
            
            ### C. Nguyên tắc tổ chức dữ liệu (Khi có Bảng biểu)
            Nếu mẫu Word của bạn có Bảng biểu (như ví dụ danh sách thiết bị ở trên), file Excel bắt buộc phải có một **"Cột khóa" (Khóa gom nhóm)**.
            - **Tại sao cần Cột khóa?** Giả sử nhân viên Nguyễn Văn A được nhận 2 thiết bị (chiếm 2 dòng trong Excel). Nếu không có Cột khóa, hệ thống sẽ in ra 2 tờ Hợp đồng riêng biệt. Nếu bạn chỉ định cột `Mã NV` làm khóa, hệ thống sẽ gom 2 dòng thiết bị đó vào chung 1 tờ Hợp đồng của anh A.
            
            *Ví dụ minh họa cấu trúc Excel:*
            👉 Ở ví dụ này, `Mã NV` chính là Cột khóa gom nhóm.
            | Mã NV (Khóa gom nhóm) | Họ và tên | Ngày sinh | STT | Tên Thiết Bị | Số Lượng |
            |---|---|---|---|---|---|
            | NV01 | Nguyễn Văn A | 01/01/1990 | 1 | Laptop Dell | 1 |
            | NV01 | Nguyễn Văn A | 01/01/1990 | 2 | Chuột | 1 |
            | NV02 | Trần Thị B | 15/05/1995 | 1 | Bàn phím | 2 |
            """)

    with st.expander("⚙️ 3. Quá trình Ghép nối (Mapping) trên Web"):
        st.markdown("""
            1. **Tải lên**: Tải file Word và Excel của bạn lên ở Bước 1.
            2. **Ánh xạ (Sự liên kết giữa Word và Excel)**: Đây là cầu nối giúp phần mềm hiểu dữ liệu. Hệ thống sẽ **tự động đoán** và ghép cặp sẵn các Cột Excel vào Biến Word tương ứng, bạn chỉ cần lướt qua kiểm tra và điều chỉnh nếu muốn.
            3. **Word nhiều biến hơn Excel thì sao?**: Đừng lo lắng! Hệ thống cho phép bạn ghép **nhiều Biến Word vào cùng một Cột Excel**. Nếu có biến Word nào tạm thời chưa có dữ liệu, bạn chỉ cần tạo một cột trống trong file Excel tải lên và ghép nó vào.
            4. **Tính năng Đổi số thành chữ & Tiền tệ**: 
               - Trong file Word, bạn có thể tạo 2 biến (VD: `{{ muc_luong }}` và `{{ muc_luong_chu }}`).
               - Trên Web, bạn được phép chọn **cùng 1 cột Excel** (VD: Cột `Mức lương`) cho cả 2 biến này.
               - Ở phần **Định dạng**: Chọn `currency` cho `muc_luong` (tạo ra `15.000.000`) và `number_to_words` cho `muc_luong_chu` (tạo ra `Mười lăm triệu`).
            5. **Khóa gom nhóm**: **RẤT QUAN TRỌNG** nếu bạn dùng bảng. Chọn "Khóa gom nhóm" là cột (VD: **`Mã NV`**) để hệ thống biết 2 dòng của `Nguyễn Văn A` thuộc về cùng 1 hợp đồng, thay vì in ra 2 hợp đồng tách biệt.
               - *Ví dụ:* Nhân viên A có 2 dòng dữ liệu (2 thiết bị). Nếu chọn khóa là `Mã NV`, hệ thống sẽ gộp 2 dòng đó vào chung 1 bảng của 1 tờ Hợp đồng cho anh A. Nếu bỏ trống, hệ thống sẽ nhồi thiết bị của cả công ty vào chung 1 tờ Hợp đồng!
            6. **Lọc dữ liệu (Tùy chọn in 1 người)**: Trước khi bấm tạo tài liệu, bạn có thể sử dụng bộ lọc ở Bước 3. Tính năng này cho phép bạn chọn in hợp đồng cho một hoặc vài nhân sự cụ thể thay vì in toàn bộ file Excel.
            7. **Sinh file**: Tùy chỉnh tên file Word và bấm nút Tải file ZIP về!
            """)

    with st.expander("⚠️ 4. Giới hạn của ứng dụng (Những gì phần mềm KHÔNG làm được)"):
        st.markdown("""
            Để hệ thống hoạt động chính xác, vui lòng lưu ý các giới hạn sau:
            - **❌ Không chèn được Hình ảnh động**: Phần mềm hiện chỉ xử lý Dữ liệu chữ và số, chưa hỗ trợ chèn ảnh (Ví dụ: Chữ ký, Avatar) lấy từ Excel vào Word.
            - **❌ Không hỗ trợ Bảng lồng Bảng**: Trong file Word, bạn không thể tạo một bảng nhỏ nằm rúc bên trong một ô của một bảng lớn khác.
            - **❌ Không hỗ trợ File bị Đặt Mật Khẩu**: Hãy chắc chắn file Word và Excel tải lên không bị khóa password bảo vệ.
            - **❌ Tiêu đề Excel không được Gộp ô (Merge Cells)**: Dòng Tiêu đề (Header) của Excel dùng để nhận diện tên cột phải phẳng và nằm trên 1 dòng duy nhất.
            - **❌ Dữ liệu siêu khổng lồ**: Vì lý do bảo mật tuyệt đối, ứng dụng không lưu file của bạn ra đĩa cứng mà xử lý 100% trên bộ nhớ RAM. Nếu file Excel của bạn có hàng chục nghìn dòng, tiến trình nén file có thể chậm hoặc báo lỗi hết bộ nhớ.
            """)

    st.info(
        "💡 **Mẹo:** Bạn có thể chạy tệp `generate_samples.py` trong mã nguồn để tự động lấy một bộ file Word và Excel mẫu chuẩn xác nhất!"
    )
