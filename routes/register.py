from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.models_user import User
from service.database.db_user import add_user, check_user_exists
from service.temp_stored.tempStored import get_temp_data, delete_temp_data
from security.validate_input import compare_and_validate
register_router = APIRouter()

@register_router.post("/register", response_model=dict)
async def register(user: User):
    clean_user_data = compare_and_validate(user.model_dump())
    temp_data = get_temp_data(user.otp_key)
    if not temp_data:
        raise HTTPException(
            status_code=400,
            detail={"error": "OTP key is invalid or expired"}
        )
    if await check_user_exists(clean_user_data['username']):
        raise HTTPException(
            status_code=400, 
            detail={"error": "Email or Username already exists."}
        )
    try:
        if temp_data['email'] == clean_user_data['email'] and temp_data['otp'] == clean_user_data['otp_mailVerify']:
            await add_user(user)
            delete_temp_data(user.otp_key)
            return JSONResponse(
                content = {"message": "User registered successfully"},
                status_code = 200
                )
    except: raise HTTPException(
            status_code=400, 
            detail={"error": "Please try again."}
        )
    