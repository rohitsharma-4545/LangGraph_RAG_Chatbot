import os
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings



def create_token(user_id: str, role: str = "user"):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=settings.EXP_HOURS)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])