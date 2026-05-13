# 📄 FlexiDoc: Nền tảng Tự động hóa Khởi tạo Tài liệu

**FlexiDoc** là một nền tảng tự động hóa tạo tài liệu "một cho tất cả". Công cụ giúp các phòng ban (Nhân sự, Pháp chế, Kinh doanh) dễ dàng trộn dữ liệu từ file Excel vào các biểu mẫu Word để tự động sinh hàng loạt hợp đồng, phụ lục. Với cơ chế ánh xạ thông minh, xử lý bảng biểu động và bảo mật 100% In-Memory (Zero-Disk), FlexiDoc loại bỏ hoàn toàn các sai sót thủ công trong công việc văn phòng.

## ✨ Tính năng Nổi bật (Killer Features)
- 🧠 **Ánh xạ Thông minh (Auto-Mapping)**: Tự động đoán và ghép cặp cột Excel với biến Word.
- 📊 **Bảng biểu Động (Dynamic Tables)**: Tự động gom nhóm dữ liệu và nhân bản dòng trong bảng Word giữ nguyên định dạng kẻ khung.
- 🔤 **Đổi Số thành Chữ Tiếng Việt**: Tích hợp sẵn bộ chuyển đổi tiền tệ và số thành chữ chuẩn xác.
- 🔒 **Bảo mật Tối đa (Zero-Disk Footprint)**: Mọi thao tác trộn, sinh file và nén ZIP đều diễn ra 100% trên bộ nhớ RAM, không lưu lại dấu vết trên máy chủ (không xả rác ổ cứng).
- ⚡ **Lọc & Cá nhân hóa**: Tùy ý chọn in hợp đồng cho một cá nhân, một phòng ban hoặc toàn bộ công ty.

## 🚀 Hướng dẫn Khởi chạy (Quick Start)
### 1. Chạy trên môi trường Dev (Local)
Đảm bảo bạn đã kích hoạt môi trường ảo `.venv` và cài đặt đủ thư viện trong `requirements.txt`.
```bash
python run.py
```
*Lệnh này sẽ tự động chạy song song **FastAPI Backend** (Port 8000) và **Streamlit UI** (Port 8501).*

### 2. Đóng gói ứng dụng (Build .exe)
Để xuất phần mềm ra file thực thi chạy độc lập trên Windows (không cần cài Python):
```bash
python build.py
```
*File `FlexiDoc.exe` sẽ được tạo ra trong thư mục `dist/`.*

## 🤖 Quy trình Tự động hóa (Workflow & Automation)
Dự án này được sinh ra bởi AI Project Generator và đã được trang bị sẵn các công cụ tự động hóa khắt khe để đảm bảo chất lượng mã nguồn:

| Công cụ / Lệnh | Chức năng tự động thực thi |
| --- | --- |
| **`check.bat`** (hoặc `auto_checks.py`) | 1. **Format Code**: Tự động căn lề chuẩn PEP8 bằng `black`.<br>2. **Auto Architecture**: Quét mã nguồn và vẽ lại cấu trúc vào README.<br>3. **Unit Tests**: Chạy `pytest` kiểm tra logic. |
| **`sync.bat`** | 1. Chạy Auto Checks (Chặn đẩy code nếu có lỗi).<br>2. Tự động tăng version (`version.txt`).<br>3. Commit mã nguồn và đẩy lên GitHub. |
| **`build.bat`** (hoặc `build.py`) | 1. **Clean**: Tự động xóa rác (`__pycache__`, logs, `.env`).<br>2. Chạy Auto Checks bảo vệ mã nguồn.<br>3. Đóng gói thành file `.exe` bằng PyInstaller. |
| **`init_github.bat`** | Tự động khởi tạo Git, tạo Repo trên GitHub bằng CLI, và tạo Release v1.0.0. |
| **`.github/workflows/`** | Tự động chạy Test và Build `.exe` trên mây mỗi khi có code mới đẩy lên. |

> **Lưu ý dành cho AI Assistant (Cursor/Copilot)**:
> Theo quy tắc tại `AI_RULES.md`, AI bắt buộc phải:
> 1. Tự động cập nhật file `PLAN.md` mỗi khi luồng logic hoặc tiến độ thay đổi (Living Documentation).
> 2. Tự động cập nhật `requirements.txt` khi import thư viện mới.

## 💻 Môi trường ảo (.venv)
Nếu bạn đã khởi tạo kèm `.venv`, hãy kích hoạt nó bằng lệnh sau:
- **Windows**: `.\.venv\Scripts\activate`
- **Mac/Linux**: `source .venv/bin/activate`

## 🏗️ Cấu trúc dự án (Architecture)
<!-- ARCHITECTURE_START -->
> Tài liệu này được cập nhật tự động bởi script `scan_architecture.py`.

### 🌳 Cây Thư Mục
```text
📦 FlexiDoc
    ┣ 📜 README.md
    ┣ 📜 PLAN.md
    ┣ 📜 requirements.txt
    ┣ 📜 .env.example
    ┣ 📜 scan_architecture.py
    ┣ 📜 auto_checks.py
    ┣ 📜 AI_RULES.md
    ┣ 📜 .gitignore
    ┣ 📜 .dockerignore
    ┣ 📜 Dockerfile
    ┣ 📜 docker-compose.yml
    ┣ 📜 LICENSE
    ┣ 📜 build.py
    ┣ 📜 sync.bat
    ┣ 📜 check.bat
    ┣ 📜 build.bat
    ┣ 📜 init_github.bat
    ┣ 📜 version.txt
    ┣ 📜 generate_docs.py
    ┣ 📜 run.py
    ┣ 📜 templates.py
    ┣ 📜 generate_samples.py
    ┣ 📜 config.toml
    ┣ 📂 src
        ┣ 📜 __init__.py
        ┣ 📜 main.py
        ┣ 📜 router.py
        ┣ 📜 templates.py
        ┣ 📜 excel.py
        ┣ 📜 profiles.py
        ┣ 📜 documents.py
        ┣ 📂 models
            ┣ 📜 __init__.py
            ┣ 📜 mapping_rule.py
            ┣ 📜 profile_model.py
        ┣ 📂 services
            ┣ 📜 __init__.py
            ┣ 📜 word_service.py
            ┣ 📜 excel_service.py
            ┣ 📜 generator_service.py
        ┣ 📂 utils
            ┣ 📜 __init__.py
            ┣ 📜 retry_example.py
            ┣ 📜 logger.py
            ┣ 📜 string_utils.py
            ┣ 📜 number_to_words.py
        ┣ 📂 controllers
            ┣ 📜 __init__.py
        ┣ 📂 config
            ┣ 📜 __init__.py
        ┣ 📂 exceptions
            ┣ 📜 __init__.py
            ┣ 📜 custom_errors.py
        ┣ 📂 database
            ┣ 📜 db.py
            ┣ 📜 __init__.py
        ┣ 📂 schemas
            ┣ 📜 document.py
            ┣ 📜 profile_schema.py
            ┣ 📜 __init__.py
        ┣ 📂 api
            ┣ 📜 __init__.py
            ┣ 📂 v1
                ┣ 📜 router.py
                ┣ 📜 __init__.py
                ┣ 📂 endpoints
                    ┣ 📜 templates.py
                    ┣ 📜 excel.py
                    ┣ 📜 profiles.py
                    ┣ 📜 documents.py
                    ┣ 📜 __init__.py
    ┣ 📂 tests
        ┣ 📜 test_FlexiDoc.py
        ┣ 📜 __init__.py
        ┣ 📜 test_utils.py
        ┣ 📜 test_word_service.py
        ┣ 📜 test_excel_service.py
        ┣ 📜 test_generator_service.py
        ┣ 📜 test_api.py
    ┣ 📂 logs
    ┣ 📂 output
    ┣ 📂 data
        ┣ 📜 flexidoc.sqlite
    ┣ 📂 static
    ┣ 📂 templates
        ┣ 📜 index.html
    ┣ 📂 .github
        ┣ 📂 workflows
            ┣ 📜 build.yml
    ┣ 📂 frontend
        ┣ 📜 api_client.py
        ┣ 📜 app.py
        ┣ 📜 __init__.py
        ┣ 📂 components
            ┣ 📜 upload_section.py
            ┣ 📜 mapping_ui.py
            ┣ 📜 generate_ui.py
            ┣ 📜 __init__.py
            ┣ 📜 guide_tab.py
    ┣ 📂 .pytest_cache
        ┣ 📜 README.md
        ┣ 📜 .gitignore
        ┣ 📜 CACHEDIR.TAG
        ┣ 📂 v
            ┣ 📂 cache
                ┣ 📜 nodeids
                ┣ 📜 lastfailed
    ┣ 📂 samples
        ┣ 📜 Du_Lieu_Nhan_Su.xlsx
        ┣ 📜 Mau_Hop_Dong.docx
    ┣ 📂 assets
        ┣ 📜 .gitkeep
        ┣ 📜 icon.png
        ┣ 📜 icon.ico
```
### 🧩 Chi Tiết Modules (Tổng quan)

| 📄 Tệp tin (File) | 📝 Chức năng / Mô tả |
| --- | --- |
| `auto_checks.py` | Kịch bản kiểm tra tự động (Định dạng mã và Kiểm thử). |
| `build.py` | Kịch bản tự động hóa quá trình đóng gói ứng dụng bằng PyInstaller. |
| `frontend/api_client.py` | API Client để xử lý giao tiếp giữa giao diện Streamlit và Backend FastAPI. |
| `frontend/app.py` | Điểm vào chính cho Ứng dụng Web Streamlit. |
| `frontend/components/generate_ui.py` | Thành phần giao diện kích hoạt sinh tài liệu và tải kết quả. |
| `frontend/components/guide_tab.py` | Thành phần giao diện hiển thị Hướng dẫn sử dụng. |
| `frontend/components/mapping_ui.py` | Thành phần giao diện để ánh xạ cột Excel với biến Word. |
| `frontend/components/upload_section.py` | Thành phần giao diện xử lý tải tệp lên và kích hoạt kiểm tra lỗi. |
| `generate_docs.py` | Kịch bản sinh tài liệu API (Swagger HTML và OpenAPI JSON) ngoại tuyến. |
| `generate_samples.py` | Kịch bản sinh file Word và Excel mẫu để test thực tế trên giao diện. |
| `run.py` | Kịch bản khởi chạy đồng thời FastAPI và Streamlit cho môi trường dev. |
| `scan_architecture.py` | Script tự động quét thư mục dự án và sinh báo cáo kiến trúc. |
| `src/api/v1/endpoints/documents.py` | API endpoints trộn dữ liệu và sinh tài liệu. |
| `src/api/v1/endpoints/excel.py` | API endpoints kiểm tra và xác thực dữ liệu Excel. |
| `src/api/v1/endpoints/profiles.py` | API endpoints quản lý dữ liệu (CRUD) Mẫu cấu hình ánh xạ. |
| `src/api/v1/endpoints/templates.py` | API endpoints kiểm tra và xác thực mẫu Word. |
| `src/api/v1/router.py` | Khối gom nhóm router chính cho API v1. |
| `src/database/db.py` | Thiết lập cơ sở dữ liệu, cấu hình engine và quản lý phiên. |
| `src/documents.py` | Chưa có mô tả chi tiết. |
| `src/excel.py` | Chưa có mô tả chi tiết. |
| `src/exceptions/custom_errors.py` | Các lớp ngoại lệ tự định nghĩa cho lỗi nghiệp vụ cụ thể. |
| `src/main.py` | Điểm bắt đầu của ứng dụng Web FastAPI FlexiDoc. |
| `src/models/mapping_rule.py` | Mô hình cơ sở dữ liệu cho MappingRule (Quy tắc ánh xạ). |
| `src/models/profile_model.py` | Mô hình cơ sở dữ liệu cho Profile (Mẫu cấu hình). |
| `src/profiles.py` | Chưa có mô tả chi tiết. |
| `src/router.py` | Chưa có mô tả chi tiết. |
| `src/schemas/document.py` | Pydantic schemas cho việc Validate và Sinh tài liệu. |
| `src/schemas/profile_schema.py` | Pydantic schemas cho Mẫu cấu hình và Quy tắc ánh xạ. |
| `src/services/excel_service.py` | Dịch vụ lõi để xử lý và trích xuất dữ liệu từ tệp Excel. |
| `src/services/generator_service.py` | Dịch vụ lõi để trộn dữ liệu vào mẫu Word và nén thành file ZIP. |
| `src/services/word_service.py` | Dịch vụ lõi để xử lý và xác thực mẫu Word. |
| `src/templates.py` | Chưa có mô tả chi tiết. |
| `src/utils/logger.py` | Cấu hình hệ thống ghi log của ứng dụng. |
| `src/utils/number_to_words.py` | Tiện ích chuyển đổi số thành chữ tiếng Việt. |
| `src/utils/retry_example.py` | Mẫu sử dụng cơ chế Retry khi gọi HTTP Request kết hợp requests và tenacity. |
| `src/utils/string_utils.py` | Các hàm tiện ích thao tác với chuỗi. |
| `templates.py` | Chưa có mô tả chi tiết. |
| `tests/test_api.py` | Kịch bản kiểm thử cho các endpoint API sử dụng TestClient. |
| `tests/test_excel_service.py` | Kịch bản kiểm thử cho Dịch vụ Excel. |
| `tests/test_FlexiDoc.py` | Chưa có mô tả chi tiết. |
| `tests/test_generator_service.py` | Kịch bản kiểm thử cho Dịch vụ Sinh tài liệu. |
| `tests/test_utils.py` | Kiểm thử tự động cho các hàm tiện ích. |
| `tests/test_word_service.py` | Kịch bản kiểm thử cho Dịch vụ Word. |

### 📚 Tài liệu API & Logic chi tiết (Dành cho Dev/AI)
Phần này trích xuất tự động thông tin về Đầu vào (Inputs) và Đầu ra (Outputs) của các hàm/lớp trong từng module để hỗ trợ tích hợp và phát triển.

#### 📄 `auto_checks.py`
**Functions:**

- **`def main() -> Any`**
  > Chưa có mô tả.


#### 📄 `build.py`
**Functions:**

- **`def get_next_version(file_path: str, bump_type: str) -> str`**
  > Chưa có mô tả.

- **`def create_version_file(version: str) -> str`**
  > Chưa có mô tả.

- **`def clean_pycache(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def clean_logs(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def clean_temp_files(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def ensure_init_files() -> None`**
  > Chưa có mô tả.

- **`def create_unified_entry() -> str`**
  > Tạo file script tạm thời để khởi chạy cả FastAPI và Streamlit song song.

- **`def build_app() -> None`**
  > Chưa có mô tả.


#### 📄 `frontend/api_client.py`
**Functions:**

- **`def validate_templates(docx_file: Any, xlsx_file: Any, sheet_name: str, header_row: int) -> Dict[str, Any]`**
  > EN: Call API to validate uploaded templates.
  > VI: Gọi API để kiểm tra các tệp mẫu đã tải lên.

- **`def get_format_types() -> List[str]`**
  > EN: Fetch available formatting types.
  > VI: Lấy danh sách các loại định dạng được hỗ trợ.

- **`def generate_document(payload: Dict[str, Any]) -> bytes`**
  > EN: Call API to generate and ZIP documents.
  > VI: Gọi API để sinh và nén tài liệu.


#### 📄 `frontend/app.py`
**Functions:**

- **`def init_session_state() -> None`**
  > Khởi tạo các biến trạng thái cần thiết cho phiên làm việc.

- **`def main() -> None`**
  > EN: Main function to configure and render the Streamlit UI.
  > VI: Hàm chính để cấu hình và hiển thị giao diện Streamlit.


#### 📄 `frontend/components/generate_ui.py`
**Functions:**

- **`def get_unique_values(excel_bytes: bytes, sheet_name: str, header_row: int, col_name: str) -> List[str]`**
  > Trích xuất danh sách các giá trị duy nhất từ một cột trong Excel để làm bộ lọc.

- **`def handle_generation(mapping_config: Dict[str, Any], upload_data: Dict[str, Any]) -> None`**
  > EN: Render generation button and download link.
  > VI: Hiển thị nút tạo tài liệu và link tải về.


#### 📄 `frontend/components/guide_tab.py`
**Functions:**

- **`def render_guide_tab() -> None`**
  > Hiển thị nội dung hướng dẫn người dùng.


#### 📄 `frontend/components/mapping_ui.py`
**Functions:**

- **`def _normalize_string(s: str) -> str`**
  > Loại bỏ dấu tiếng Việt và ký tự đặc biệt để so sánh chuỗi.

- **`def _guess_col_index(word_var: str, excel_cols: List[str]) -> int`**
  > Đoán cột Excel phù hợp nhất với biến Word.

- **`def render_mapping_rules(upload_data: Dict[str, Any]) -> Dict[str, Any]`**
  > EN: Render mapping UI with dynamic data from API client.
  > VI: Hiển thị giao diện Mapping với dữ liệu động từ API client.


#### 📄 `frontend/components/upload_section.py`
**Functions:**

- **`def render_onboarding_ui() -> None`**
  > EN: Render onboarding instructions for 0-variable Word templates.
  > VI: Hiển thị hướng dẫn nhúng biến cho mẫu Word không có biến nào.

- **`def handle_file_upload() -> Optional[Dict[str, Any]]`**
  > EN: Render file uploaders and handle validation flow.
  > VI: Hiển thị khu vực tải file và xử lý luồng kiểm tra lỗi.


#### 📄 `generate_docs.py`
**Functions:**

- **`def generate_api_docs() -> None`**
  > Chưa có mô tả.


#### 📄 `generate_samples.py`
**Functions:**

- **`def generate_word() -> Any`**
  > Chưa có mô tả.

- **`def generate_excel() -> Any`**
  > Chưa có mô tả.


#### 📄 `run.py`
**Functions:**

- **`def start_fastapi() -> Any`**
  > Chưa có mô tả.

- **`def wait_for_port(port, host, timeout) -> Any`**
  > Chưa có mô tả.


#### 📄 `scan_architecture.py`
**Functions:**

- **`def get_directory_tree(start_path: str, exclude_dirs: set) -> str`**
  > Sinh cây thư mục (bỏ qua các thư mục không cần thiết).

- **`def parse_python_file(file_path: str) -> dict`**
  > Phân tích file Python bằng AST để lấy thông tin Class, Function và Docstring.

- **`def update_readme(target_dir: str, readme_file: str) -> Any`**
  > Quét kiến trúc và cập nhật thẳng vào file README.md.


#### 📄 `src/api/v1/endpoints/profiles.py`
**Functions:**

- **`def get_profiles(db: Session) -> Any`**
  > Lấy danh sách tất cả các Mẫu cấu hình (Profiles) đã lưu.

- **`def create_profile(profile_in: ProfileCreate, db: Session) -> Any`**
  > Tạo và lưu trữ một Mẫu cấu hình cùng các Quy tắc ánh xạ (Mapping Rules) mới.


#### 📄 `src/database/db.py`
**Functions:**

- **`def init_db() -> None`**
  > EN: Initialize the database, creating all tables if they don't exist.
  > VI: Khởi tạo cơ sở dữ liệu, tạo tất cả các bảng nếu chúng chưa tồn tại.

- **`def get_db() -> Generator`**
  > EN: Dependency to get DB session for FastAPI endpoints.
  > VI: Hàm dependency để lấy phiên DB cho các endpoint FastAPI.


#### 📄 `src/exceptions/custom_errors.py`
**Classes:**

- **`class FlexiDocBaseError`**
  > Lớp cơ sở cho các lỗi của FlexiDoc.

- **`class InvalidFileFormatError`**
  > Lỗi khi định dạng file (Word/Excel) tải lên không hợp lệ hoặc bị hỏng.

- **`class TemplateSyntaxError`**
  > Lỗi cú pháp thẻ biến Jinja2 trong mẫu Word.

- **`class ZeroVariableError`**
  > Lỗi khi file Word không chứa bất kỳ thẻ ngoặc nhọn nào ({{...}}).

- **`class SheetNotFoundError`**
  > Lỗi khi không tìm thấy tên Sheet được cấu hình trong file Excel.

- **`class EmptyHeaderRowError`**
  > Lỗi khi dòng tiêu đề (Header row) của Excel hoàn toàn trống.


#### 📄 `src/main.py`
**Functions:**

- **`def read_root() -> Any`**
  > Chưa có mô tả.

- **`def main() -> Any`**
  > Chưa có mô tả.


#### 📄 `src/models/mapping_rule.py`
**Classes:**

- **`class MappingRule`**
  > EN: SQLAlchemy Model for Mapping Rules corresponding to a Profile.
  > VI: Lớp Model SQLAlchemy cho các Quy tắc Ánh xạ thuộc về một Mẫu cấu hình.


#### 📄 `src/models/profile_model.py`
**Classes:**

- **`class Profile`**
  > EN: SQLAlchemy Model for Mapping Profiles.
  > VI: Lớp Model SQLAlchemy cho các Mẫu Cấu hình Ánh xạ.


#### 📄 `src/schemas/document.py`
**Classes:**

- **`class TemplateValidationResponse`**
  > Schema phản hồi khi phân tích thành công Mẫu Word.

- **`class ExcelValidationResponse`**
  > Schema phản hồi khi phân tích thành công file Excel.

- **`class GeneratePayload`**
  > Schema chứa dữ liệu cấu hình sinh tài liệu.
  > Lưu ý: File sẽ được gửi qua form-data thay vì JSON body.


#### 📄 `src/schemas/profile_schema.py`
**Classes:**

- **`class MappingRuleBase`**
  > Schema cơ sở cho Quy tắc ánh xạ.

- **`class MappingRuleResponse`**
  > Schema phản hồi cho Quy tắc ánh xạ (có kèm ID từ DB).

- **`class ProfileCreate`**
  > Schema đầu vào khi tạo mới một Mẫu cấu hình.

- **`class ProfileResponse`**
  > Schema phản hồi khi lấy thông tin Mẫu cấu hình.


#### 📄 `src/services/excel_service.py`
**Functions:**

- **`def validate_sheet(excel_bytes: bytes, sheet_name: str) -> bool`**
  > EN: Check if the specified sheet exists in the workbook.
  > VI: Kiểm tra xem sheet được chỉ định có tồn tại trong tệp không.

- **`def normalize_headers(sheet_obj: openpyxl.worksheet.worksheet.Worksheet, header_row: int) -> list[str]`**
  > EN: Extract and normalize header strings.
  > VI: Trích xuất và chuẩn hóa dòng tiêu đề.

- **`def extract_raw_data(excel_bytes: bytes, sheet_name: str, header_row: int) -> list[dict]`**
  > EN: Extract raw data, handling merged cells and skipping empty rows.
  > VI: Trích xuất dữ liệu thô, xử lý tự động điền ô gộp và bỏ qua dòng trống.


#### 📄 `src/services/generator_service.py`
**Functions:**

- **`def apply_formatting(value: str, format_type: str) -> Union[str, RichText]`**
  > EN: Apply specific formats (currency, words, newlines) to the string.
  > VI: Áp dụng định dạng (tiền tệ, chữ, xuống dòng) cho chuỗi dữ liệu.

- **`def group_data_by_key(data: List[Dict[str, Any]], grouping_key: str) -> Dict[str, List[Dict[str, Any]]]`**
  > EN: Group rows of data by a specific key.
  > VI: Gom nhóm các dòng dữ liệu dựa trên một cột khóa.

- **`def render_and_zip(template_bytes: bytes, grouped_data: Dict[str, List[Dict[str, Any]]], rules: List[Dict[str, Any]], filename_pattern: str) -> bytes`**
  > EN: Render Word templates in memory and compress them into a ZIP archive.
  > VI: Trộn dữ liệu vào Word trên bộ nhớ đệm và nén thành file ZIP.


#### 📄 `src/services/word_service.py`
**Functions:**

- **`def extract_variables(template_bytes: bytes) -> Dict[str, List[str]]`**
  > EN: Extract all single and table variables from the Word template.
  > VI: Trích xuất tất cả các biến đơn và biến bảng biểu từ mẫu Word.

- **`def preprocess_template(template_bytes: bytes) -> bytes`**
  > EN: Convert custom simple table syntax to Jinja2 syntax.
  > VI: Chuyển đổi cú pháp bảng biểu đơn giản thành cú pháp chuẩn của Jinja2.

- **`def validate_syntax(template_bytes: bytes) -> None`**
  > EN: Perform a dry-run to validate Jinja2 syntax in the template.
  > VI: Chạy thử để kiểm tra tính hợp lệ của cú pháp Jinja2.


#### 📄 `src/utils/logger.py`
**Functions:**

- **`def get_logger(name: str) -> logging.Logger`**
  > Khởi tạo và trả về đối tượng logger.


#### 📄 `src/utils/number_to_words.py`
**Functions:**

- **`def _read_group(group: int, full: bool) -> str`**
  > Hàm phụ trợ để đọc một cụm 3 chữ số.

- **`def number_to_words_vn(number: float) -> str`**
  > EN: Convert a number to Vietnamese text.
  > VI: Chuyển đổi số thành chữ tiếng Việt (hỗ trợ đến hàng tỷ).


#### 📄 `src/utils/retry_example.py`
**Functions:**

- **`def fetch_data_with_retry(url: str) -> dict`**
  > Chưa có mô tả.


#### 📄 `src/utils/string_utils.py`
**Functions:**

- **`def sanitize_filename(name: str) -> str`**
  > EN: Remove invalid characters from OS filename.
  > VI: Loại bỏ các ký tự cấm của hệ điều hành trong tên file để tránh lỗi ZIP.


#### 📄 `tests/test_api.py`
**Functions:**

- **`def setup_teardown_db() -> Any`**
  > Chưa có mô tả.

- **`def create_dummy_docx() -> bytes`**
  > Chưa có mô tả.

- **`def create_dummy_excel() -> bytes`**
  > Chưa có mô tả.

- **`def test_validate_template_api() -> Any`**
  > Chưa có mô tả.

- **`def test_validate_excel_api() -> Any`**
  > Chưa có mô tả.

- **`def test_profiles_crud_api() -> Any`**
  > Chưa có mô tả.

- **`def test_generate_documents_api() -> Any`**
  > Kiểm thử API trộn và sinh file ZIP (Tạo hợp đồng/Phụ lục).


#### 📄 `tests/test_excel_service.py`
**Functions:**

- **`def create_dummy_excel(sheet_name, data, merged_cells) -> bytes`**
  > Tạo file Excel ảo trên RAM.

- **`def test_validate_sheet_not_found() -> Any`**
  > Test lỗi khi không tìm thấy sheet.

- **`def test_normalize_headers() -> Any`**
  > Test chuẩn hóa dòng tiêu đề.

- **`def test_normalize_headers_empty() -> Any`**
  > Test lỗi dòng tiêu đề rỗng.

- **`def test_extract_raw_data_merged() -> Any`**
  > Test trích xuất và unmerge tự động điền dữ liệu (forward-fill).

- **`def test_extract_raw_data_empty_rows() -> Any`**
  > Test bỏ qua dòng trống tinh.


#### 📄 `tests/test_FlexiDoc.py`
**Functions:**

- **`def test_example() -> Any`**
  > EN: Example test to enforce TDD.
  > VI: Test mẫu để ép tuân thủ TDD.


#### 📄 `tests/test_generator_service.py`
**Functions:**

- **`def test_apply_formatting_currency() -> Any`**
  > Kiểm tra ép kiểu tiền tệ.

- **`def test_apply_formatting_words() -> Any`**
  > Kiểm tra gọi hàm đổi số thành chữ.

- **`def test_apply_formatting_richtext() -> Any`**
  > Kiểm tra nhận diện xuống dòng tạo RichText.

- **`def test_group_data_by_key() -> Any`**
  > Kiểm tra gom nhóm dòng dữ liệu.


#### 📄 `tests/test_utils.py`
**Functions:**

- **`def test_sanitize_filename() -> Any`**
  > EN: Test filename sanitization logic.
  > VI: Kiểm thử logic làm sạch tên file hệ điều hành.

- **`def test_number_to_words_vn() -> Any`**
  > EN: Test converting numbers to Vietnamese words.
  > VI: Kiểm thử logic đổi số thành chữ tiếng Việt.


#### 📄 `tests/test_word_service.py`
**Functions:**

- **`def create_dummy_docx(text: str) -> bytes`**
  > Tạo một file Word ảo trên RAM để test.

- **`def test_extract_variables_zero() -> Any`**
  > Test lỗi khi không có biến nào.

- **`def test_extract_variables_success() -> Any`**
  > Test trích xuất biến đơn và biến bảng thành công.

- **`def test_validate_syntax_error() -> Any`**
  > Test bắt lỗi sai cú pháp thẻ Jinja2 (thiếu dấu ngoặc).

<!-- ARCHITECTURE_END -->
