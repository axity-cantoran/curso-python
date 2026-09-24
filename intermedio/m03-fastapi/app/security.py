from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "cambia-esta-clave-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    return str(hashed)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    resultado = pwd_context.verify(
        plain_password,
        hashed_password,
    )
    return bool(resultado)


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    expires = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, object] = {
        "sub": subject,
        "exp": expires,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return str(token)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError as error:
        raise ValueError("Token inválido") from error

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise ValueError("El token no contiene subject")

    return subject
