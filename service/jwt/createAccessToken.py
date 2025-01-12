from datetime import datetime, timedelta
from jose import JWTError, jwt
from service.dotenv_manage.dotenv_manage import get_env_variable

# Secret key để mã hóa JWT (Bạn nên giữ bí mật này và không hardcode trong code)
SECRET_KEY = get_env_variable('JWT_SECRET_KEY')
ALGORITHM = get_env_variable('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hàm tạo JWT token
def create_access_token(username: str, email: str, user_id: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    # Lấy thời gian đăng nhập hiện tại
    login_at = datetime.now()
    
    # Dữ liệu sẽ được mã hóa trong JWT token
    to_encode = {
        "sub": username,  # username
        "email": email,    # email
        "user_id": user_id,  # Thêm _id vào token
        "loginAt": login_at.isoformat(),  # thời gian đăng nhập (ISO 8601 format)
    }
    
    # Thêm thông tin hết hạn vào dữ liệu
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    
    # Mã hóa và tạo JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

