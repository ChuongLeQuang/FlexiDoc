# Project Plan: FlexiDoc

## 🎯 Mục tiêu dự án
- Mô tả ngắn gọn mục tiêu của dự án.
- Tầm nhìn và kết quả mong đợi.
- **Mục tiêu**: Xây dựng một nền tảng Web (Web Platform) tự động hóa việc tạo hàng loạt Phụ lục Hợp đồng và các tài liệu tương tự từ file Excel và mẫu Word.
- **Tầm nhìn**: Trở thành công cụ "một cho tất cả" (all-in-one), giúp nhân viên các phòng ban (Pháp chế, Nhân sự, Kinh doanh) tự chủ hoàn toàn trong việc tạo tài liệu mà không cần sự can thiệp của IT, giảm thiểu sai sót thủ công và tăng tốc độ xử lý công việc.
- **Kết quả mong đợi**: Một ứng dụng Web với giao diện trực quan, cho phép người dùng tải lên file Excel/Word, tự định nghĩa quy tắc ánh xạ (mapping), lưu lại để tái sử dụng, và xuất ra hàng loạt file Word đã được điền đúng dữ liệu, đúng định dạng, đóng gói trong file ZIP.

## 📋 Yêu cầu cốt lõi (Core Requirements)
- [x] Tách biệt Core API (FastAPI) và Frontend UI (Streamlit).
- [x] Validation Excel nghiêm ngặt: Tự động đối chiếu cấu trúc cột file mới với Profile cũ trước khi chạy.
- [x] Xử lý Multi-sheet: Bắt buộc chọn và đối chiếu chính xác tên Sheet chứa dữ liệu.
- [x] Cơ chế Mapping trực quan: Lưu trữ cấu hình (Profile) vào SQLite, loại bỏ việc thao tác file JSON thủ công.
- [x] Thay thế `pandas` bằng `openpyxl` để kiểm soát 100% kiểu dữ liệu (dtype) thô từ Excel.
- [x] Xử lý 100% In-Memory (Zero-Disk Footprint) bảo mật dữ liệu.
- [x] Xử lý dữ liệu dị thường (Edge Cases): Hỗ trợ tùy chỉnh dòng Header, tự động Unmerge & Fill ô gộp, loại bỏ dòng trống, chuẩn hóa tên cột (xóa khoảng trắng thừa).
- [x] Hỗ trợ Đa ngôn ngữ & Unicode (UTF-8): Xử lý an toàn tên file, nội dung tiếng Việt/ngoại ngữ trong Excel/Word và tránh lỗi font khi nén ZIP.
- [x] Tách bạch API Contract: Chuẩn hóa giao thức giao tiếp và xử lý lỗi (Error Handling) giữa FastAPI và Streamlit.
- [x] Tối ưu UX/UI cho Template Word: Bẫy lỗi cú pháp Jinja2 (Dry-run), hướng dẫn Onboarding khi file Word không chứa biến.
- [x] Xử lý Word Nâng cao: Cung cấp cú pháp bảng biểu đơn giản (`{{table_start:list_name}}`) và tự động tiền xử lý (pre-process) thành cú pháp Jinja2 phức tạp, hỗ trợ RichText.
- [x] Tích hợp Cẩm nang sử dụng (In-App User Guide): Cung cấp Tab hướng dẫn trực quan trên UI kèm tính năng tải Bộ file mẫu chuẩn (Word + Excel) để người dùng thực hành.
- [x] Tùy biến Tên file & Chống ghi đè: Cho phép người dùng cấu hình quy tắc đặt tên file Word đầu ra (dựa trên biến dữ liệu) và tự động xử lý trùng lặp (Name Collisions) khi nén ZIP.

## 📊 Báo cáo Đối chiếu chéo (Cross-Audit Report)
| # | Yêu cầu cốt lõi | Hạng mục WBS đối chiếu (Thực thi) | Trạng thái |
|---|---|---|---|
| 1 | Tách biệt Core API và Frontend UI | **2.7** (Controllers) & **2.8** (Streamlit app.py) | ✅ Khớp |
| 2 | Validation Excel nghiêm ngặt & Xử lý Multi-sheet | **2.5** (validate_sheet), **2.7** (`/excel/validate`) | ✅ Khớp |
| 3 | Cơ chế Mapping trực quan, lưu DB SQLite | **2.1** (Models), **2.2** (Schemas), **2.8** (mapping_ui) | ✅ Khớp |
| 4 | Xử lý 100% In-Memory (Zero-Disk Footprint) | **2.4, 2.5** (nhận bytes), **2.6** (zip), **2.7** (Streaming) | ✅ Khớp |
| 5 | Xử lý Excel dị thường (header, unmerge, dòng rỗng) | **2.5** (normalize_headers, extract_raw), **2.9** (Tests) | ✅ Khớp |
| 6 | Chuẩn hóa giao thức giao tiếp & xử lý lỗi (API Contract) | **2.2** (ErrorResponse), **2.3** (Errors), **2.7** (Handler) | ✅ Khớp |
| 7 | Bẫy lỗi Jinja2 (Dry-run), 0-variable Onboarding | **2.4** (validate_syntax), **2.7** (Bắt lỗi), **2.8** (UI) | ✅ Khớp |
| 8 | Cú pháp bảng biểu đơn giản & Hỗ trợ RichText | **2.4** (preprocess_template), **2.6** (apply_formatting) | ✅ Khớp |
| 9 | Tích hợp Cẩm nang sử dụng (Hướng dẫn & File mẫu) | **2.8** (guide_tab.py) | ✅ Khớp |
| 10| Hỗ trợ Unicode (UTF-8) & Thuật toán Số thành chữ | **2.3** (number_to_words.py), **2.6** (apply_formatting) | ✅ Khớp |
| 11| Tùy biến Tên file đầu ra & Xử lý trùng lặp (Collision) | **2.1** (DB), **2.2** (API), **2.6** (Zip logic), **2.8** (UI) | ✅ Khớp |

## � Kiến trúc & Luồng dữ liệu (Data Flow)
1. **Select & Upload (UI)**: Người dùng chọn "Mapping Profile" đã lưu (hoặc tạo mới). Do nguyên tắc Zero-Disk, người dùng **luôn tải lên cặp file `docx` và `xlsx`** (hệ thống sẽ check tên file Word xem có khớp với mẫu đã lưu không).
2. **Validation & Matching**: FastAPI kiểm tra tên Sheet và đối chiếu danh sách cột của Excel mới với Profile. Báo lỗi UI nếu sai tên Sheet hoặc thiếu cột.
3. **Visual Mapping UI**: Nếu tạo mới/chỉnh sửa, UI hiển thị 2 khu vực:
    - **Biến đơn**: Cần chọn Sheet chứa dữ liệu trước, sau đó ghép nối `[Biến Word] <-> [Cột Excel] <-> [Định dạng]`.
    - **Bảng biểu động**: Cho phép người dùng chọn "Cột khóa" (Grouping Key) và ánh xạ các trường trong vòng lặp `{%tr for %}`.
4. **Raw Data Processing**: Tiền xử lý Template Word (dịch cú pháp `{{table_start}}` thành Jinja2). Tiền xử lý Excel (Xác định dòng Header, Chuẩn hóa tên cột, Unmerge & Fill, lọc dòng trống). Sau đó dùng `openpyxl` đọc dữ liệu thô và gom nhóm.
5. **Render & Zip (In-Memory)**: Lặp qua từng nhóm dữ liệu, sinh file Word tương ứng, và nén vào bộ đệm `zipfile` trên RAM. Trả về UI và dọn dẹp (GC).

## 🚀 Tiến độ (Phases)

### Phase 1: Khởi tạo & Thiết kế
- [x] Khởi tạo cấu trúc dự án
- [x] Khởi tạo cấu trúc dự án (Định nghĩa thư mục `src/`, `tests/`, file `requirements.txt`, thiết lập quy tắc `AI_RULES.md` và các kịch bản tự động hóa CI/CD cục bộ như `build.py`, `sync.bat`).
- [x] Thiết kế Database (SQLite) cho Mapping Profiles.
- [x] Thiết kế luồng xử lý (Data Flow)
- [x] Thiết kế giao diện UI Mapping toàn diện (Wireframe), bao gồm cả Biến đơn và Bảng biểu động.
- [x] Thiết kế kiến trúc Database Schema (Table: Profiles (có `sheet_name`, `header_row`), Mapping_Rules).
- [x] Thiết kế API Contract (Danh sách Endpoints kết nối FastAPI & Streamlit, format JSON Error chuẩn).
- [x] Thiết kế logic xác thực đầu vào nâng cao (Validate Word Template: Pre-processing cú pháp đơn giản, bắt lỗi Jinja2 Syntax & 0-variable onboarding).
- [x] Thiết kế UX Đào tạo người dùng: Tích hợp Tab Hướng dẫn & Tải File Mẫu trực tiếp vào giao diện Streamlit.
- [x] Thực hiện Đối chiếu chéo (Cross-audit) và lập Báo cáo đảm bảo độ phủ 100% cho Phase 2 (WBS).
- [x] Lập Lộ trình thi công (Execution Sequence) theo phương pháp "Outside-In TDD".

### Phase 2: Phát triển (Development) - Chi tiết hóa (WBS)

**2.1. Cấu hình Database & Models (SQLAlchemy)**
- [x] Khởi tạo thư mục `src/database/` và file `db.py` (Engine, SessionLocal, Base).
- [x] Khởi tạo thư mục `src/models/` và file `profile_model.py` (Model `Profile`: `id` (PK), `name` (unique), `template_filename`, `sheet_name`, `header_row`, `grouping_key`, `filename_pattern` (str, nullable)).
- [x] Bổ sung file `mapping_rule.py` (Model `MappingRule`: `id` (int, PK), `profile_id` (int, FK), `variable_type` (str), `word_var` (str), `excel_col` (str), `format_type` (str, default='text')).
- [x] Viết hàm `init_db()` để hệ thống tự động tạo file SQLite gốc khi chạy lần đầu.

**2.2. Định nghĩa API Contract (Pydantic Schemas)**
- [x] Khởi tạo thư mục `src/schemas/`.
- [x] Tạo file `base.py`:
    - **Mục đích**: Định nghĩa các schema cơ sở dùng chung, đặc biệt là chuẩn hóa Response Lỗi.
    - **Schema `ErrorDetail`**: `loc` (list[str]), `msg` (str), `type` (str).
    - **Schema `ErrorResponse` (Output)**: `error_code` (str), `message` (str), `details` (dict | list[ErrorDetail] | None).
- [x] Tạo file `profile_schema.py`:
    - **Mục đích**: Định nghĩa Input/Output cho API quản lý Mẫu cấu hình ánh xạ (CRUD Profiles).
    - **Schema `MappingRuleBase`**: `variable_type` (str), `word_var` (str), `excel_col` (str), `format_type` (str, default='text').
    - **Schema `MappingRuleResponse` (Output)**: Kế thừa `MappingRuleBase`, thêm `id` (int).
    - **Schema `ProfileCreate` (Input)**: `name`, `template_filename`, `sheet_name`, `header_row`, `grouping_key`, `filename_pattern` (str | None), `rules`.
    - **Schema `ProfileResponse` (Output)**: Bổ sung thêm trường `filename_pattern` trả về cho UI.
- [x] Tạo file `document.py`:
    - **Mục đích**: Định nghĩa Input/Output cho các API Bóc tách mẫu (Validate) và Sinh tài liệu (Generate).
    - **Schema `TemplateValidationResponse` (Output)**: `single_vars` (list[str]), `table_vars` (dict[str, list[str]]).
    - **Schema `ExcelValidationResponse` (Output)**: `sheet_names` (list[str]), `columns` (list[str]).
    - **Schema `GeneratePayload` (Input - Parse từ form-data)**: Bổ sung thêm `filename_pattern` (str).

**2.3. Cấu hình Core (Exceptions, Logger & Utils)**
- [x] Khởi tạo thư mục `src/exceptions/` và file `custom_errors.py`:
    - **Mục đích**: Định nghĩa các lớp lỗi `InvalidFileFormatError`, `TemplateSyntaxError`, `ZeroVariableError`, `SheetNotFoundError`, `EmptyHeaderRowError`.
- [x] Khởi tạo thư mục `src/utils/` và file `logger.py`:
    - **Mục đích**: Cấu hình Python `logging` xuất file log ra thư mục `logs/` theo chuẩn quy định tại AI Rules.
- [x] Tạo file `src/utils/number_to_words.py`:
    - **Mục đích**: Chứa thuật toán tiếng Việt chuyển đổi số nguyên/số thực thành chuỗi chữ (Ví dụ: 15000 -> "Mười lăm nghìn").
- [x] Tạo file `src/utils/string_utils.py`:
    - **Mục đích**: Chứa hàm `sanitize_filename(name: str) -> str` loại bỏ ký tự cấm của OS (`\/:*?"<>|`) để chống lỗi file ZIP.

**2.4. Lõi xử lý Core: Dịch vụ Word (Word Service)** (Đã hoàn thành)
- [x] Khởi tạo thư mục `src/services/` và file `word_service.py` chứa các hàm:
    - `preprocess_template(template_bytes: bytes) -> bytes`: 
        - **Mục đích**: Tìm thẻ `{{table_start:x}}`, `{{table_end}}` thay bằng `{%tr for %}` của Jinja2.
        - **Lỗi**: Sai định dạng file -> raise `InvalidFileFormatError`.
    - `validate_syntax(template_bytes: bytes) -> None`: 
        - **Mục đích**: Chạy thử thư viện `docxtpl` (Dry-run) để kiểm tra cú pháp thẻ ngoặc nhọn.
        - **Lỗi**: Sai cú pháp -> raise `TemplateSyntaxError` (kèm thông tin đoạn text bị lỗi).
    - `extract_variables(template_bytes: bytes) -> dict`: 
        - **Mục đích**: Trích xuất tất cả các biến đã dùng trong file Word.
        - **Output**: `{"single_vars": list[str], "table_vars": dict[str, list[str]]}`.
        - **Lỗi**: Độ dài biến = 0 -> raise `ZeroVariableError` để UI kích hoạt luồng Onboarding.

**2.5. Lõi xử lý Core: Dịch vụ Excel (Excel Service)** (Đã hoàn thành)
- [x] Khởi tạo file `src/services/excel_service.py` chứa các hàm:
    - `validate_sheet(excel_bytes: bytes, sheet_name: str) -> bool`:
        - **Mục đích**: Load workbook chế độ read-only kiểm tra tên sheet có tồn tại không.
        - **Lỗi**: Không thấy sheet -> raise `SheetNotFoundError`.
    - `normalize_headers(sheet_obj: Worksheet, header_row: int) -> list[str]`:
        - **Mục đích**: Quét dòng tiêu đề, loại bỏ khoảng trắng thừa 2 đầu và khoảng trắng kép.
        - **Lỗi**: Dòng rỗng -> raise `EmptyHeaderRowError`.
    - `extract_raw_data(excel_bytes: bytes, sheet_name: str, header_row: int) -> list[dict]`:
        - **Mục đích**: Đọc dữ liệu, thực hiện unmerge cells (forward-fill), bỏ dòng rỗng tinh.
        - **Output**: Danh sách các dòng dữ liệu dạng mảng từ điển (List of Dictionaries), dữ liệu ép 100% về `str`.

**2.6. Lõi xử lý Core: Dịch vụ Sinh tài liệu (Document Generation)** (Đã hoàn thành)
- [x] Khởi tạo file `src/services/generator_service.py` chứa các hàm:
    - `apply_formatting(value: str, format_type: str) -> str | docxtpl.RichText`:
        - **Mục đích**: Ép kiểu Tiền tệ/Ngày tháng, gọi utils chuyển Số thành chữ. Đặc biệt: Tự động phát hiện chuỗi chứa `\n` để chuyển thành `RichText` giữ nguyên định dạng xuống dòng.
    - `group_data_by_key(data: list[dict], grouping_key: str) -> dict[str, list[dict]]`:
        - **Mục đích**: Gom các dòng Excel vào chung một nhóm dựa trên "Cột khóa".
    - `render_and_zip(template_bytes: bytes, grouped_data: dict, rules: list, filename_pattern: str) -> bytes`:
        - **Mục đích**: Render mẫu Word. Khớp dữ liệu đặt tên file -> Gọi `sanitize_filename`. Tự động thêm hậu tố `_1`, `_2` nếu trùng lặp. Nén In-Memory.
        - **Output**: Chuỗi byte của file ZIP (zipfile bytes).

**2.7. Xây dựng API Endpoints (FastAPI Controllers)** (Đã hoàn thành)
- [x] Tạo thư mục `src/api/v1/endpoints/`.
- [x] Thiết lập file `src/main.py`: Cấu hình **CORSMiddleware** (cho phép Streamlit gọi API) và Global Exception Handler ép lỗi về chuẩn JSON.
- [x] `POST /api/v1/templates/validate`: Nhận `UploadFile`. Gọi `word_service`. Trả về `TemplateValidationResponse`. (Đặc biệt: Bắt `ZeroVariableError` trả về JSON với `error_code="ZERO_VARIABLES"`).
- [x] `POST /api/v1/excel/validate`: Nhận `UploadFile`, `sheet_name`, `header_row`. Gọi `excel_service`. Trả về `ExcelValidationResponse`.
- [x] `GET /api/v1/profiles`: Lấy danh sách mẫu. Trả về `list[ProfileResponse]`.
- [x] `POST /api/v1/profiles`: Nhận `ProfileCreate`. Lưu Database. Trả về `ProfileResponse`.
- [x] `POST /api/v1/documents/generate`: Nhận `UploadFile` (docx, xlsx) + form data `GeneratePayload`. Trả về `StreamingResponse` (MIME: `application/zip`).

**2.8. Xây dựng Giao diện Web (Streamlit UI)**
- [ ] Khởi tạo file `app.py` (ở thư mục gốc theo AI Rules) và thư mục `frontend/components/`:
    - `app.py` (Main Entry): 
        - **Mục đích**: Set cấu hình trang (`st.set_page_config`), khởi tạo 2 Tabs chính ("⚡ Chạy hệ thống" và "📖 Hướng dẫn").
    - `components/guide_tab.py` -> `render_guide_tab() -> None`:
        - **Mục đích**: Hiển thị Markdown hướng dẫn cấu hình Word/Excel. Cung cấp `st.download_button` để tải file ZIP chứa mẫu Word/Excel chuẩn.
    - `components/upload_section.py` -> `handle_file_upload() -> dict`:
        - **Mục đích**: Hiển thị `st.file_uploader` nhận file `docx` và `xlsx`. Gọi API `POST /templates/validate` và `POST /excel/validate`.
        - **Xử lý Lỗi**: Parse schema `ErrorResponse`. Nếu mã là `ZERO_VARIABLES`, gọi hàm con `render_onboarding_ui()` (Hiển thị các bước hướng dẫn nhúng biến vào Word). Các lỗi khác in `st.error`.
    - `components/mapping_ui.py` -> `render_mapping_rules(word_vars: dict, excel_cols: list) -> list[dict]`:
        - **Mục đích**: Render bảng ghép nối. Hiển thị ô Text Input cho phép người dùng định nghĩa quy tắc đặt tên file đầu ra (VD: `Phụ_lục_{{ho_ten}}`).
        - **Output**: Danh sách các rules Mapping được người dùng chốt.
    - `components/generate_ui.py` -> `handle_generation(payload: dict) -> None`:
        - **Mục đích**: Hiện nút "Tạo tài liệu". Khi click, gọi API `POST /documents/generate` cùng `st.spinner`.
        - **Output**: Nếu thành công, hiện `st.success` và `st.download_button` trả file ZIP.

**2.9. Kiểm thử & Cấu hình (Tests & CI/CD)**
- [ ] Khởi tạo thư mục `tests/` và viết các hàm Unit Test kiểm chứng ngoại lệ:
    - `test_word_service.py`: (Đã hoàn thành)
        - `test_preprocess_template_success()`: Input template có `{{table_start:ds}}`, output kiểm tra có tự chuyển thành `{%tr for item in ds %}`.
        - `test_validate_syntax_error()`: Input file Word cố tình viết thiếu `{%tr endfor %}`, kiểm tra assert văng `TemplateSyntaxError`.
        - `test_extract_variables_zero()`: Input file Word thô không có thẻ ngoặc nhọn, kiểm tra assert văng `ZeroVariableError`.
    - `test_excel_service.py`: (Đã hoàn thành)
        - `test_normalize_headers()`: Input list `[" Họ và tên  ", "Lương   mới"]`, assert output `["Họ và tên", "Lương mới"]`.
        - `test_extract_raw_data_merged()`: Tạo dữ liệu ảo có ô bị gộp (Merged Cells), assert output dict tự động điền lấp (forward-fill).
        - `test_extract_raw_data_empty_rows()`: Tạo dữ liệu ảo chứa dòng trắng tinh (chỉ có border format), assert output hàm bỏ qua 100% dòng rỗng đó.
- [ ] Viết các Unit Test còn lại để đảm bảo độ phủ (Coverage):
    - [x] `test_generator_service.py`: Mock test file Word output.
    - [x] `test_utils.py`: Test hàm `sanitize_filename` (đưa vào chuỗi `A/B:C*D` trả ra `A_B_C_D`) và `number_to_words`.
    - [x] `test_api.py`: Test endpoints thông qua `TestClient` của FastAPI.
- [x] Chỉnh sửa `build.py` để khai báo các thư mục `frontend`, `templates` vào PyInstaller.

## 🗺️ Lộ trình thi công (TDD Execution Sequence)
*Tuân thủ phương pháp Outside-In TDD (Phát triển từ ngoài vào trong) để bám sát trải nghiệm người dùng (UI-First) theo `AI_RULES.md`.*

**Bước 1: Giao thức & Giao diện (Contracts & UI Shells)**
- [x] 1.1. Khởi tạo `src/schemas/` (Pydantic) để chốt chặt Input/Output dựa trên Wireframe (Tham chiếu WBS 2.2).
- [x] 1.2. Dựng UI Components (`frontend/`) với Mock Data để xác nhận luồng thao tác. (Lưu ý: Ép buộc luồng UI upload 2 file Word+Excel dù dùng mẫu cũ) (Tham chiếu WBS 2.8).
- [x] 1.3. Viết `test_api.py` ➔ Tạo `src/api/v1/endpoints/` trả về Mock Data. Cấu hình bắt buộc **CORSMiddleware** tại `main.py` (Tham chiếu WBS 2.7 & 2.9).

**Bước 2: Lõi nghiệp vụ & Nền tảng (Business Services & Core - TDD)**
- [x] 2.1. Viết `test_utils.py` (Test hàm `sanitize_filename` & số thành chữ) ➔ Code `src/exceptions/`, `src/utils/` (Tham chiếu WBS 2.3 & 2.9).
- [x] 2.2. Viết Test ➔ Code `src/services/word_service.py` (Xong) & `excel_service.py` (Xong).
- [x] 2.3. Viết `test_generator_service.py` ➔ Code `src/services/generator_service.py` (Xong).

**Bước 3: Lưu trữ & Tích hợp (Database & Integration)**
- [x] 3.1. Viết Test DB ➔ Code `src/database/db.py` và `src/models/` (Tham chiếu WBS 2.1).
- [x] 3.2. Tích hợp: Nối Services và DB vào các API Endpoints và xóa Mock Data. Hoàn thiện hệ thống.

### Phase 3: Hoàn thiện & Triển khai (Deployment)
- [x] Đóng gói ứng dụng / Cấu hình CI/CD (Đang tiến hành)
- [ ] Viết tài liệu (README, API Docs)
- [ ] Triển khai lên môi trường Production

## 📝 Nhật ký (Changelog / Notes)
- **2026-05-12**: Khởi tạo cấu trúc dự án.
- **Cập nhật mới nhất**: Thống nhất kiến trúc tách decoupled FastAPI & Streamlit; chốt luồng Data Flow In-Memory (Bảo mật Zero-Disk Footprint).
- **Cập nhật UX & Data**: Quyết định loại bỏ JSON file upload, dùng DB lưu Profile. Đổi `pandas` thành `openpyxl` để tránh lỗi Dtype.
- **Cập nhật UI & Validation**: Chốt thiết kế bảng Mapping trực quan (3 thành phần: Biến - Cột - Format). Thêm luồng chặn lỗi (Validation) khi file Excel tải lên bị sai cấu trúc cột so với Profile.
- **Cập nhật UI (Nâng cao)**: Hoàn thiện thiết kế UI cho việc xử lý "Bảng biểu động" (Dynamic Tables) bằng cơ chế "Grouping Key".
- **Cập nhật Database**: Chốt thiết kế DB SQLite gồm 2 bảng `profiles` và `mapping_rules`. Tích hợp phân loại biến (`single`/`table`) để render UI động.
- **Cập nhật Logic Multi-sheet**: Thêm thuộc tính `sheet_name` vào Profile và logic bẫy lỗi sai tên Sheet trong quá trình vận hành để phòng tránh lỗi từ phía người dùng.
- **Cập nhật Logic Xử lý Ngoại lệ**: Bổ sung cơ chế tiền xử lý Excel: Cho phép chọn dòng Header (`header_row`), chuẩn hóa tên cột (strip khoảng trắng thừa), tự động xử lý ô trộn (Merged Cells) và tự động bỏ qua dòng trống (Empty Rows).
- **Cập nhật Unicode/Encoding**: Bổ sung yêu cầu bắt buộc xử lý an toàn dữ liệu đa ngôn ngữ (UTF-8) cho toàn bộ luồng I/O (Tên file, API Payload, nén ZIP) để ngăn chặn hoàn toàn lỗi font chữ.
- **Cập nhật Logic Word Template**: Bổ sung luồng Dry-run Parse để bắt lỗi Jinja2 Syntax và màn hình Onboarding hướng dẫn người dùng tự đặt biến nếu file Word chưa có thẻ `{{ }}`.
- **Cập nhật API Contract**: Chuẩn hóa cấu trúc Error JSON (`error_code`, `message`, `details`) và định nghĩa danh sách 6 Endpoints cốt lõi kết nối FastAPI - Streamlit.
- **Cập nhật Logic Word Nâng cao**: Bổ sung cơ chế quét cây cú pháp Jinja2 (AST) để tách biệt Biến đơn và Biến vòng lặp bảng (`{%tr for %}`). Bổ sung giải pháp xử lý định dạng RichText và Multi-line (Alt+Enter từ Excel).
- **Cập nhật UX (Word Template)**: Thay thế cơ chế AST phức tạp bằng cú pháp bảng biểu đơn giản hóa (`{{table_start}}`, `{{table_end}}`) và logic tiền xử lý tự động để thân thiện hơn với người dùng cuối.
- **Cập nhật In-App Guide**: Quyết định thiết kế Tab Hướng dẫn sử dụng trực quan ngay trên Streamlit UI kèm bộ file mẫu chuẩn (Word/Excel) để giáo dục người dùng (User Education) thay vì dùng tài liệu PDF tĩnh.
- **Hoàn tất Phase 1**: Rà soát, hiệu chỉnh và làm rõ toàn bộ các hạng mục trong Kế hoạch Dự án. Chính thức đóng lại Giai đoạn Thiết kế.
- **Cập nhật AI Rules**: Đưa triết lý làm việc (chi tiết hóa WBS và hoàn thiện thiết kế trước khi code) vào `AI_RULES.md` để trở thành tiêu chuẩn bắt buộc cho toàn dự án.
- **Chi tiết hóa UI & Test WBS**: Chuẩn hóa WBS cho Phase 2.7 (Streamlit UI chia nhỏ component) và 2.8 (Unit Test định nghĩa rõ test cases) chi tiết đến từng hàm theo đúng Hiến pháp.
- **Kiểm toán chéo (Cross-audit)**: Khớp nối yêu cầu cốt lõi với WBS, bổ sung nhóm 2.3 (Cấu hình Core) chứa Utils, Logging, Custom Exceptions và thuật toán RichText để đảm bảo tính thực thi 100% khi code.
- **Lập Lộ trình thi công (TDD Sequence)**: Bổ sung Lộ trình thi công theo từng bước (Step-by-step), ép buộc quy trình TDD (Viết test -> Code) vào thực tiễn để tránh rủi ro code xong mới test.
- **Hoàn tất Hiến pháp & Lộ trình**: Bổ sung quy tắc "Lập Lộ trình thi công" vào AI Rules và chốt lộ trình theo phương pháp "Outside-In TDD" để bám sát trải nghiệm người dùng.
