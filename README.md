# FlexiDoc

Module/Project documentation goes here.

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
<!-- ARCHITECTURE_END -->
