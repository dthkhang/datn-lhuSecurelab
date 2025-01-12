from typing import Any
from uuid import uuid4
import time

# In-memory storage
_temp_store = {}

def save_temp_data(data: Any, ttl: int = 300) -> str:
    """
    Lưu dữ liệu tạm thời.
    Args:
        data: Dữ liệu cần lưu trữ.
        ttl: Thời gian sống của dữ liệu (giây).
    Returns:
        key: Khóa duy nhất để truy cập dữ liệu.
    """
    key = str(uuid4())  # Tạo UUID làm khóa duy nhất
    expire_at = time.time() + ttl
    _temp_store[key] = {"data": data, "expire_at": expire_at}
    return key

def get_temp_data(key: str) -> Any:
    """
    Lấy dữ liệu từ bộ nhớ tạm.
    Args:
        key: Khóa duy nhất của dữ liệu.
    Returns:
        data: Dữ liệu đã lưu hoặc None nếu không tồn tại.
    """
    if key not in _temp_store:
        return None
    record = _temp_store[key]
    if time.time() > record["expire_at"]:  # Kiểm tra nếu dữ liệu hết hạn
        del _temp_store[key]
        return None
    return record["data"]

def delete_temp_data(key: str) -> bool:
    """
    Xóa dữ liệu tạm thời.
    Args:
        key: Khóa duy nhất của dữ liệu.
    Returns:
        bool: True nếu xóa thành công, False nếu không tìm thấy.
    """
    if key in _temp_store:
        del _temp_store[key]
        return True
    return False
