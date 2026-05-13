"""
EN: Auto checks script (Formatting & Testing).
VI: Kịch bản kiểm tra tự động (Định dạng mã và Kiểm thử).
"""

import subprocess
import sys


def main():
    print("🛡️ Đang bắt đầu quá trình kiểm tra tự động (Auto Checks)...")

    print("\n👉 1. Kiểm tra định dạng mã nguồn (Black Formatter)...")
    try:
        subprocess.run([sys.executable, "-m", "black", ".", "--check"], check=True)
        print("✅ Định dạng mã nguồn chuẩn xác!")
    except subprocess.CalledProcessError:
        print("⚠️ CẢNH BÁO: Mã nguồn chưa đúng chuẩn format.")
        print("👉 Đang tự động format lại mã nguồn...")
        subprocess.run([sys.executable, "-m", "black", "."])

    print("\n👉 2. Cập nhật tài liệu kiến trúc (README.md)...")
    try:
        subprocess.run([sys.executable, "scan_architecture.py"], check=True)
    except subprocess.CalledProcessError:
        print(
            "\n❌ LỖI: Không thể cập nhật tài liệu kiến trúc. Vui lòng kiểm tra file scan_architecture.py."
        )
        sys.exit(1)

    print("\n👉 3. Chạy kiểm thử tự động (Pytest)...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/"], check=True)
        print("✅ Tất cả các bài kiểm thử đều vượt qua (All tests passed)!")
    except subprocess.CalledProcessError:
        print(
            "\n❌ LỖI: Có bài kiểm thử (Test) không vượt qua. Vui lòng sửa mã nguồn trước khi Build hoặc Đẩy code."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
