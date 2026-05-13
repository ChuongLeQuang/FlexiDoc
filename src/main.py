"""
EN: Main entry point for FastAPI Web application FlexiDoc.
VI: Điểm bắt đầu của ứng dụng Web FastAPI FlexiDoc.
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

from src.api.v1.router import api_router
from src.database.db import init_db
from src.exceptions.custom_errors import ZeroVariableError, FlexiDocBaseError

# Hỗ trợ PyInstaller resolve đường dẫn tĩnh
if getattr(sys, "frozen", False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Khởi tạo các tài nguyên cần thiết khi ứng dụng khởi động."""
    init_db()
    yield


app = FastAPI(title="FlexiDoc", lifespan=lifespan)

# 1. Cấu hình CORS để Streamlit (hoặc Web độc lập) có thể gọi API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên giới hạn domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Gắn API Router v1
app.include_router(api_router, prefix="/api/v1")


# 3. Khai báo Bẫy lỗi (Global Exception Handlers)
@app.exception_handler(ZeroVariableError)
async def zero_variable_handler(request: Request, exc: ZeroVariableError):
    return JSONResponse(
        status_code=400,
        content={"error_code": "ZERO_VARIABLES", "message": str(exc), "details": None},
    )


@app.exception_handler(FlexiDocBaseError)
async def custom_error_handler(request: Request, exc: FlexiDocBaseError):
    # Chuyển đổi tên class lỗi (VD: SheetNotFoundError -> SHEET_NOT_FOUND_ERROR)
    error_code = (
        "".join(["_" + c if c.isupper() else c for c in exc.__class__.__name__])
        .strip("_")
        .upper()
    )
    return JSONResponse(
        status_code=400,
        content={"error_code": error_code, "message": str(exc), "details": None},
    )


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = os.path.join(base_dir, "templates", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"<h1>🚀 Hello from FlexiDoc Web App!</h1>"


def main():
    print("🚀 Khởi động Web Server tại http://localhost:8000")
    # Tắt tính năng reload để tránh vi phạm quy tắc tiến trình con của Daemon process
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
