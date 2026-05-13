"""
EN: Unified local development script.
VI: Kịch bản khởi chạy đồng thời FastAPI và Streamlit cho môi trường dev.
"""

import multiprocessing
import sys
import time
import socket
import subprocess


def start_fastapi():
    import src.main

    src.main.main()


def wait_for_port(port, host="127.0.0.1", timeout=15.0):
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
    multiprocessing.freeze_support()

    print("🚀 Đang khởi động FlexiDoc (Local Dev)...")

    api_process = multiprocessing.Process(target=start_fastapi)
    api_process.daemon = True
    api_process.start()

    if not wait_for_port(8000):
        print("⚠️ FastAPI khởi động quá chậm. Vẫn tiếp tục mở UI...")

    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Đang tắt hệ thống...")
    finally:
        api_process.terminate()
        sys.exit(0)
