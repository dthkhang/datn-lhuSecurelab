import bcrypt

# Mã hóa mật khẩu
def hash_password(password: str) -> str:
    """
    Mã hóa mật khẩu sử dụng bcrypt
    :param password: Mật khẩu gốc
    :return: Mật khẩu đã mã hóa
    """
    salt = bcrypt.gensalt()  # Tạo salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Mã hóa mật khẩu
    return hashed_password.decode('utf-8')  # Chuyển mật khẩu đã mã hóa thành chuỗi

# So sánh mật khẩu đã mã hóa và mật khẩu nhập vào
def check_password(plain_password: bytes, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)
