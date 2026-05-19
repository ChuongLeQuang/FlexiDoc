"""
EN: Build script to automate PyInstaller packaging.
VI: Kịch bản tự động hóa quá trình đóng gói ứng dụng bằng PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from datetime import datetime


def get_next_version(file_path: str = "version.txt", bump_type: str = "current") -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            current_version = f.read().strip()
    else:
        current_version = "1.0.0"

    if bump_type == "current":
        return current_version

    parts = current_version.split(".")
    if len(parts) >= 3:
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    return "1.0.1"


def create_version_file(version: str) -> str:
    parts = version.split(".")
    while len(parts) < 4:
        parts.append("0")
    vers_tuple = f"({parts[0]}, {parts[1]}, {parts[2]}, {parts[3]})"

    content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(filevers={vers_tuple}, prodvers={vers_tuple}, mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[StringFileInfo([StringTable('040904B0', [
    StringStruct('CompanyName', 'Le Quang Chuong'),
    StringStruct('FileDescription', 'FlexiDoc - Công cụ tự động hóa tài liệu (Phiên bản Cá nhân)'),
    StringStruct('FileVersion', '{version}'),
    StringStruct('InternalName', 'FlexiDoc'),
    StringStruct('LegalCopyright', 'Copyright (c) 2026 Le Quang Chuong. All rights reserved.'),
    StringStruct('OriginalFilename', 'FlexiDoc.exe'),
    StringStruct('ProductName', 'FlexiDoc'),
    StringStruct('ProductVersion', '{version}')])]), 
  VarFileInfo([VarStruct('Translation', [1033, 1200])])]
)"""
    file_path = "version_info.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def clean_pycache(start_path: str = ".") -> None:
    print("🧹 Đang dọn dẹp các thư mục __pycache__...")
    count = 0
    for root, dirs, files in os.walk(start_path, topdown=False):
        for name in dirs:
            if name == "__pycache__":
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu file đang bị khóa
    if count > 0:
        print(f"✨ Đã xóa {count} thư mục __pycache__.")


def clean_logs(start_path: str = ".") -> None:
    logs_dir = os.path.join(start_path, "logs")
    if os.path.exists(logs_dir):
        print("🧹 Đang dọn dẹp các file log cũ...")
        count = 0
        for f in os.listdir(logs_dir):
            if f.endswith(".log"):
                try:
                    os.remove(os.path.join(logs_dir, f))
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu file đang bị khóa
        if count > 0:
            print(f"✨ Đã xóa {count} file log.")


def clean_temp_files(start_path: str = ".") -> None:
    print("🧹 Đang dọn dẹp các file tạm (.env, .sqlite)...")
    count = 0
    for root, dirs, files in os.walk(start_path):
        if ".venv" in root or ".git" in root:
            continue
        for f in files:
            if f == ".env" or f.endswith(".sqlite") or f.endswith(".sqlite3"):
                try:
                    os.remove(os.path.join(root, f))
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu bị khóa
    if count > 0:
        print(f"✨ Đã xóa {count} file tạm.")


def ensure_init_files() -> None:
    for base_dir in ["src", "apps", "shared", "core"]:
        if os.path.exists(base_dir):
            for root, dirs, files in os.walk(base_dir):
                init_file = os.path.join(root, "__init__.py")
                if not os.path.exists(init_file):
                    with open(init_file, "w", encoding="utf-8") as f:
                        pass


def create_unified_entry() -> str:
    """Tạo file script tạm thời để khởi chạy cả FastAPI và Streamlit song song."""
    content = """import multiprocessing
import streamlit.web.cli as stcli
import sys
import os
import time
import socket
import frontend.app as app
import src.main as main

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    return os.path.abspath(path)

def start_fastapi():
    main.main()

def wait_for_port(port, host='127.0.0.1', timeout=15.0):
    # Chờ cho đến khi Backend FastAPI thực sự mở port.
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                return False

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Bắt buộc để chạy multiprocessing trong PyInstaller Windows
    
    # 1. Khởi chạy FastAPI ngầm
    api_process = multiprocessing.Process(target=start_fastapi)
    api_process.daemon = True  # Tiến trình này sẽ tự chết khi ứng dụng chính đóng
    api_process.start()
    
    # 2. Chờ (Ping) cho đến khi Backend khởi động xong cổng 8000, tối đa 15 giây
    is_api_ready = wait_for_port(8000)
    if not is_api_ready:
        print("⚠️ Cảnh báo: Backend FastAPI khởi động quá chậm. Vẫn tiếp tục mở UI...")
    
    # 3. Khởi chạy giao diện Streamlit
    script_path = resolve_path("frontend/app.py")
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())
"""
    with open("run_unified.py", "w", encoding="utf-8") as f:
        f.write(content)
    return "run_unified.py"


def build_app() -> None:
    if "--bump-only" in sys.argv:
        bump_type = "patch"
        if "--major" in sys.argv:
            bump_type = "major"
        elif "--minor" in sys.argv:
            bump_type = "minor"
        new_version = get_next_version(bump_type=bump_type)
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write(new_version)
        print(f"✅ Đã cập nhật version.txt lên: {new_version}")
        sys.exit(0)

    print("🚀 Khởi động quá trình đóng gói ứng dụng...")
    try:
        import PyInstaller
    except ImportError:
        print(
            "\n❌ Không tìm thấy thư viện 'pyinstaller'. Vui lòng chạy pip install pyinstaller"
        )
        sys.exit(1)

    # Kiểm tra xem file exe cũ có đang chạy ngầm không để tránh lỗi WinError 5
    old_exe = os.path.join("dist", "FlexiDoc.exe")
    if os.path.exists(old_exe):
        try:
            os.remove(old_exe)
        except PermissionError:
            print(f"\n❌ LỖI: File '{old_exe}' đang được mở hoặc chạy ngầm!")
            print(
                "👉 Vui lòng tắt hoàn toàn ứng dụng (hoặc dùng Task Manager -> End Task) trước khi Build lại."
            )
            sys.exit(1)

    for old_dir in ["build", "dist"]:
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir, ignore_errors=True)

    clean_pycache()
    clean_logs()
    clean_temp_files()
    ensure_init_files()

    python_exe = sys.executable
    if os.path.exists(os.path.join(".venv", "Scripts", "python.exe")):
        python_exe = os.path.join(".venv", "Scripts", "python.exe")

    if os.path.exists("auto_checks.py"):
        print("🔍 Đang chạy các kịch bản kiểm tra tự động (Auto Checks)...")
        try:
            subprocess.run([python_exe, "auto_checks.py"], check=True)
        except subprocess.CalledProcessError:
            print(
                "❌ LỖI: Auto Checks thất bại. Vui lòng sửa mã nguồn trước khi đóng gói."
            )
            sys.exit(1)

    bump_type = "current"
    if "--major" in sys.argv:
        bump_type = "major"
    elif "--minor" in sys.argv:
        bump_type = "minor"
    elif "--patch" in sys.argv:
        bump_type = "patch"

    new_version = get_next_version(bump_type=bump_type)
    print(f"📌 Phiên bản chuẩn bị build: {new_version}")

    app_name = "FlexiDoc"
    entry_point = create_unified_entry()
    icon_path_ico = os.path.join("assets", "icon.ico")
    icon_path_png = os.path.join("assets", "icon.png")
    separator = os.pathsep

    pyinstaller_args = [
        python_exe,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        f"--name={app_name}",
        "--paths=.",
    ]

    # Thêm các cờ bắt buộc để Streamlit có thể chạy trong file thực thi
    pyinstaller_args.append("--copy-metadata=streamlit")
    pyinstaller_args.append("--hidden-import=streamlit")
    pyinstaller_args.extend(["--collect-all", "streamlit"])

    if (
        not os.path.exists(icon_path_ico)
        and os.path.exists(icon_path_png)
        and platform.system() == "Windows"
    ):
        try:
            from PIL import Image

            img = Image.open(icon_path_png)
            img.save(icon_path_ico, format="ICO")
        except ImportError:
            pass
        except OSError as e:
            print(f"Không thể chuyển đổi icon: {e}")

    if os.path.exists(icon_path_ico):
        pyinstaller_args.append(f"--icon={icon_path_ico}")
    elif os.path.exists(icon_path_png) and platform.system() != "Windows":
        pyinstaller_args.append(f"--icon={icon_path_png}")

    for extra in ["assets", "templates", "static", "frontend", ".streamlit"]:
        if os.path.exists(extra):
            pyinstaller_args.append(f"--add-data={extra}{separator}{extra}")

    old_version = "1.0.0"
    if os.path.exists("version.txt"):
        with open("version.txt", "r", encoding="utf-8") as f:
            old_version = f.read().strip()

    with open("version.txt", "w", encoding="utf-8") as f:
        f.write(new_version)

    if os.path.exists("version.txt"):
        pyinstaller_args.append(f"--add-data=version.txt{separator}.")

    if platform.system() == "Windows":
        version_file = create_version_file(new_version)
        pyinstaller_args.append(f"--version-file={version_file}")

    pyinstaller_args.append(entry_point)

    try:
        subprocess.run(pyinstaller_args, check=True)
        print(f"\n✅ Đóng gói thành công '{app_name}'!")
        if platform.system() == "Windows" and os.path.exists("version_info.txt"):
            os.remove("version_info.txt")
        if os.path.exists(f"{app_name}.spec"):
            os.remove(f"{app_name}.spec")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists(entry_point):
            os.remove(entry_point)
    except subprocess.CalledProcessError as e:
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write(old_version)
        if os.path.exists(entry_point):
            os.remove(entry_point)
        print(f"\n❌ Có lỗi xảy ra: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_app()
