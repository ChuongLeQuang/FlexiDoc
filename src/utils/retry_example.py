"""
EN: Example of HTTP request with Retry mechanism using Tenacity.
VI: Mẫu sử dụng cơ chế Retry khi gọi HTTP Request kết hợp requests và tenacity.
"""

import logging
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
    ),
    reraise=True,
)
def fetch_data_with_retry(url: str) -> dict:
    logger.info(f"🌐 Đang gọi API: {url}")
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        result = fetch_data_with_retry("https://httpstat.us/503")
        print("✅ Lấy dữ liệu thành công.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Đã hết số lần thử lại. Lỗi cuối cùng: {e}")
