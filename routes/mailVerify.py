from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.models_user import User_VerifyMailRequest
from service.email.mail import send_otp_email
from service.otp.otp import gen_otp
from service.temp_stored.tempStored import save_temp_data
from security.validate_input import compare_and_validate

mailVerify_router = APIRouter()
@mailVerify_router.post("/mail-verify", response_model=dict)
async def mailVerify(user: User_VerifyMailRequest):
    clean_user_data = compare_and_validate(user.model_dump())
    otp = gen_otp()
    try: 
        await send_otp_email(clean_user_data['email'],otp)
        print(otp)
        otp_key = save_temp_data({"email":clean_user_data['email'],"otp":otp}, ttl=300)
        return JSONResponse(
            content = {"message": "The otp code has been sent to your email", "otp_key": otp_key},
            status_code = 200
            )
    except: raise HTTPException(
            status_code=400, 
            detail={"error": "Please try again."}
        )


