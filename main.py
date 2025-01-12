from fastapi import FastAPI
from routes.register import register_router
from routes.login import login_router
from routes.mailVerify import mailVerify_router
from security.middleware import SecurityHeadersMiddleware

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
# Include routes
app.include_router(register_router, prefix="/api", tags=["Register"])
app.include_router(login_router, prefix="/api", tags=["Login"])
app.include_router(mailVerify_router, prefix="/api", tags=["Mail Verify"])


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Application"}
