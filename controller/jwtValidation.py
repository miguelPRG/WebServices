import jwt
import os
import secrets
import base64
from datetime import datetime, timedelta, timezone

def _generate_secret() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(64)).decode().rstrip("=")

# Em produção, defina JWT_SECRET_KEY no .env
SECRET_KEY = os.getenv("JWT_SECRET_KEY") or _generate_secret()
ALGORITHM = "HS512"
EXPIRATION_HOURS = 24

def generate_jwt(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(hours=EXPIRATION_HOURS)

    payload = {
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": secrets.token_urlsafe(16),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_jwt(token: str) -> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')