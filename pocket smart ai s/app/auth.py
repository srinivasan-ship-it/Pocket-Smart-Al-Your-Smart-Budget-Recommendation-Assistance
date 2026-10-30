from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed: str
) -> bool:

    return pwd_context.verify(
        password,
        hashed
    )


def create_access_token(
    user_id: int
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
) -> int | None:

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")

        if subject is None:
            return None

        return int(subject)

    except (
        JWTError,
        ValueError,
        TypeError
    ):

        return None