from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from service.dotenv_manage.dotenv_manage import get_env_variable
import ssl,httpx,asyncio

from_email = 'lhu.securelab@gmail.com'
subject='WELLCOME TO LHU-SECURELAB'
api_key = get_env_variable('sendgrid_api_key')

# Gửi email với bỏ qua SSL
async def send_otp_email(to_emails,otp):    
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=f'<strong>Your OTP is {otp}, dont share for anyone</strong>'
    )
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Gửi yêu cầu bất đồng bộ bằng httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.sendgrid.com/v3/mail/send',
                headers={'Authorization': f'Bearer {api_key}'},
                json=message.get(),  # Convert message to the expected JSON format
            )
            
            print(response.status_code)
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

# asyncio.run(send_otp_email('dthkhang@gmail.com', 123456)) 
# 
# 
# #test code with cmd python3 -m service.email.mail