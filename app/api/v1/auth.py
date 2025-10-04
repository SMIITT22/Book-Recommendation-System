from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.schemas.login_req_schema import LoginRequest
from app.schemas.token import Token
from app.services import auth_service
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(body: LoginRequest):
    user = auth_service.get_user(body.username)
    if not user or not auth_service.verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user["username"], "id": user["id"]}
    access_token = auth_service.create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
