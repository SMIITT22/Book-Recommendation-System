from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError 
from app.schemas.token import TokenData
from app.services import auth_service
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes JWT, validates its payload using the TokenData schema, and returns
    the current user's data. Raises 401 error if token is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(**payload)
        
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = auth_service.get_user(username=token_data.sub)
    if user is None:
        raise credentials_exception
        
    return user