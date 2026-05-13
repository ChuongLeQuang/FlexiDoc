"""
EN: Script to generate offline Swagger UI HTML and OpenAPI JSON.
VI: Kịch bản sinh tài liệu API (Swagger HTML và OpenAPI JSON) ngoại tuyến.
"""

import os
import json
import sys


def generate_api_docs() -> None:
    try:
        from fastapi.openapi.utils import get_openapi
        from src.main import app
    except ImportError as e:
        print(f"❌ Lỗi: Không thể import FastAPI hoặc app từ src.main ({e})")
        sys.exit(1)

    print("🔍 Đang trích xuất lược đồ OpenAPI...")

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "openapi.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=4, ensure_ascii=False)
    print(f"✅ Đã lưu OpenAPI JSON tại: {json_path}")

    html_content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{app.title} - Swagger UI</title><link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" /><style>body {{ margin: 0; padding: 0; }}</style></head><body><div id="swagger-ui"></div><script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script><script>window.onload = function() {{ SwaggerUIBundle({{ url: "openapi.json", dom_id: '#swagger-ui', presets: [ SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset ], layout: "BaseLayout" }}); }}</script></body></html>"""

    html_path = os.path.join(output_dir, "swagger.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Đã lưu Swagger UI HTML tại: {html_path}")
    print("👉 Hãy mở file output/swagger.html bằng trình duyệt để xem tài liệu API.")


if __name__ == "__main__":
    generate_api_docs()
