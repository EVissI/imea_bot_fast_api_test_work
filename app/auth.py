import jwt
import datetime
from loguru import logger
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings  # Загружаем секретный ключ из настроек

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITM

security = HTTPBearer()

def create_jwt_token():
    """Генерация JWT-токена для бота"""
    payload = {
        "sub": "telegram_bot",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: HTTPAuthorizationCredentials = Security(security)):
    """Валидация JWT-токена"""
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Authorization token is missing")

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("sub") != "telegram_bot":
            logger.warning("Попытка использовать токен с некорректным sub")
            raise HTTPException(status_code=403, detail="Invalid token subject")

        return payload

    except jwt.ExpiredSignatureError:
        logger.error("Попытка использовать просроченный токен")
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        logger.error("Попытка использовать некорректный токен")
        raise HTTPException(status_code=403, detail="Invalid token")