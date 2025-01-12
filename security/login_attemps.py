from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException

# Dictionary lưu trữ thông tin đăng nhập
failed_login_attempts: Dict[str, Dict] = {}

# Các cấu hình
MAX_FAILED_ATTEMPTS = 5  # Số lần đăng nhập sai tối đa
BLOCK_TIME = timedelta(hours=1)  # Thời gian khóa tạm thời 1 giờ

async def check_failed_login(remote_addr: str):
    """Kiểm tra số lần đăng nhập sai và thời gian khóa tạm thời"""
    if remote_addr in failed_login_attempts:
        attempts = failed_login_attempts[remote_addr]
        if attempts["count"] >= MAX_FAILED_ATTEMPTS:
            # Kiểm tra xem có quá thời gian khóa chưa
            if datetime.now() - attempts["last_failed_at"] < BLOCK_TIME:
                raise HTTPException(status_code=403, detail="Too many failed attempts. Try again later.")
            else:
                # Reset lại sau thời gian khóa
                failed_login_attempts.pop(remote_addr)

async def increment_failed_login(remote_addr: str):
    """Tăng số lần đăng nhập sai"""
    if remote_addr not in failed_login_attempts:
        failed_login_attempts[remote_addr] = {"count": 0, "last_failed_at": datetime.now()}
    
    failed_login_attempts[remote_addr]["count"] += 1
    failed_login_attempts[remote_addr]["last_failed_at"] = datetime.now()
