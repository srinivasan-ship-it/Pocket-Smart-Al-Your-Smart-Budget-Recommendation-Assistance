from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field

from app.auth import decode_access_token
from app.database import get_db
from app.models import User


class RegisterRequest(BaseModel):

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class SessionInfo(BaseModel):

    logged_in: bool
    user_id: int
    name: str
    email: EmailStr


class HomeRequest(BaseModel):

    budget: float = Field(gt=0)
    room_type: str
    style: str
    items: list[str] = []
    city: str = "Chennai"


class PartyRequest(BaseModel):

    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str
    venue: str = "Home"
    food_preference: str = "Mixed"


class RecommendationResponse(BaseModel):

    model_config = ConfigDict(extra="allow")

    budget: float | None = None
    summary: str | None = None
    recommendations: list[dict] = []
    tips: list[str] = []
    source: str | None = None


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