from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.auth import decode_access_token
from app.database import get_db
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    auto_error=False
)


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    bearer_token = (
        token
        or request.cookies.get("access_token")
    )

    user_id = (
        decode_access_token(bearer_token)
        if bearer_token
        else None
    )

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    user = db.get(
        User,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user