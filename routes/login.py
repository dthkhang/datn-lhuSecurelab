from fastapi import APIRouter, HTTPException, Request
from models.models_user import User_LoginRequest
from security.validate_input import compare_and_validate
from security.login_attemps import check_failed_login, increment_failed_login
from service.database.db_user import find_user_by_email_or_username
from service.hash_password.hash_pwd import check_password
from service.jwt.createAccessToken import create_access_token
login_router = APIRouter()

@login_router.post("/login", response_model=dict)
async def login(request: Request, user: User_LoginRequest):  # Đối tượng user là User_LoginRequest
    remote_addr = request.client.host  # Lấy địa chỉ IP của client
    
    # Kiểm tra xem remote_addr có bị block không
    await check_failed_login(remote_addr)

    # Chuyển đổi user thành dict để kiểm tra HTML và SQL Injection
    clean_user_data = compare_and_validate(user.model_dump())  # Chuyển đổi sang dict để kiểm tra HTML và SQL Injection
    # Kiểm tra HTML và SQL Injection
    # Kiểm tra sự tồn tại của người dùng trong cơ sở dữ liệu
    user_from_db = await find_user_by_email_or_username(clean_user_data['username'])  # Tìm theo tên đăng nhập hoặc email
    if user_from_db is None:
        await increment_failed_login(remote_addr)
        raise HTTPException(
            status_code=400, 
            detail={"error": "Invalid credentials"}
        )
    if not check_password(user.password.encode('utf-8'), user_from_db["password"].encode('utf-8')):
        await increment_failed_login(remote_addr)
        raise HTTPException(status_code=400, detail={"error": "Invalid credentials"})

    # Nếu đăng nhập thành công, tạo và trả về token
    access_token = create_access_token(
        user_id=str(user_from_db["_id"]),
        username=user_from_db["username"], 
        email=user_from_db["email"]
    )
    return {"access_token":access_token, "token_type": "bearer"}
