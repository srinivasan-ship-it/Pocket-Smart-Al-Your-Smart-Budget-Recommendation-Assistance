from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.auth import create_access_token
from app.auth import hash_password
from app.auth import verify_password

from app.database import get_db

from app.dependencies import get_current_user

from app.models import User

from app.schemas import RegisterRequest
from app.schemas import LoginRequest
from app.schemas import TokenResponse
from app.schemas import SessionInfo


router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = payload.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(
            payload.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == payload.email.lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user.id
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out successfully"
    }


@router.get(
    "/session-info",
    response_model=SessionInfo
)
def session_info(
    user: User = Depends(
        get_current_user
    )
):

    return {
        "logged_in": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


@router.get("/session-data")
def session_data(
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    count = (
        db.query(User)
        .filter(User.id == user.id)
        .count()
    )

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "account_exists": bool(count)
    }


@router.post(
    "/token",
    response_model=TokenResponse
)
def token(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    return login(
        payload,
        response,
        db
    )