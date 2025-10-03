import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# dummy in-memory user "database"
def load_users_from_json() -> Dict[str, dict]:
    """
    Loads the dummy user database from a JSON file located in the project root.
    """
    project_root = Path(__file__).resolve().parent.parent.parent
    user_file = project_root / "users.json"
    
    if not user_file.exists():
        print(f"!!! WARNING: Could not find users.json at {user_file}! Using empty user DB.")
        return {}
    
    print(f"--- Loading dummy users from {user_file} ---")
    with open(user_file, "r") as f:
        return json.load(f)

dummy_users_db = load_users_from_json()

# service functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> Optional[dict]:
    """Retrieves a user from the in-memory dummy database."""
    return dummy_users_db.get(username)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt