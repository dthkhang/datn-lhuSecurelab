from pydantic import BaseModel, EmailStr, Field, field_validator

class User(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    phone: str = Field(..., pattern=r"^\+?\d{10,15}$")
    otp_mailVerify: str = Field(..., pattern=r"^\d{6}$")
    otp_key: str = Field(...)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for char in value):
            raise ValueError("Password must contain at least one special character.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "exampleuser",
                "password": "SecurePassword123!",
                "phone": "+84912345678",
                "otp_mailVerify": "123456",
                "otp_key": "e329b117-0375-46cf-8523-524e87af83ba"
            }
        }

class User_LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for char in value):
            raise ValueError("Password must contain at least one special character.")
        return value
    class Config:
        json_schema_extra = {
            "example": {
                "username": "exampleuser",
                "password": "SecurePassword123!",
            }
        }

class User_VerifyMailRequest(BaseModel):
    email: EmailStr = Field(...)
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
            }
        }

