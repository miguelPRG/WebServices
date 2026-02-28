import jwt
import os
import secrets
import base64
from datetime import datetime, timedelta, timezone
from functools import wraps

# Produção: use JWT_SECRET_KEY via Secret Manager/KMS.
def _load_or_generate_secret() -> str:
    """
    Produção: use JWT_SECRET_KEY via Secret Manager/KMS.
    Fallback (dev): gera chave forte dinâmica no startup.
    """
    env_secret = os.getenv("JWT_SECRET_KEY")
    if env_secret and len(env_secret) >= 64:  # ~>= 384 bits em texto
        return env_secret

    # 512 bits de entropia, codificado em base64url
    generated = base64.urlsafe_b64encode(secrets.token_bytes(64)).decode().rstrip("=")
    return generated

# Configuration
SECRET_KEY = _load_or_generate_secret()
ALGORITHM = "HS512"  # mais forte que HS256 para HMAC
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