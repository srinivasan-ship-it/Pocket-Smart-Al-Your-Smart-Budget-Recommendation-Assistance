import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies import get_current_user

from app.models import User
from app.models import RecommendationHistory

from app.schemas import HomeRequest
from app.schemas import PartyRequest
from app.schemas import RecommendationResponse

from services.gemini import gemini_service


router = APIRouter(
    tags=["Planners"]
)


def save_history(
    db: Session,
    user: User,
    planner: str,
    payload: dict,
    result: dict
):

    row = RecommendationHistory(
        user_id=user.id,
        planner_type=planner,
        budget=float(
            payload["budget"]
        ),
        request_json=json.dumps(
            payload,
            ensure_ascii=False
        ),
        result_json=json.dumps(
            result,
            ensure_ascii=False
        )
    )

    db.add(row)

    db.commit()


@router.post(
    "/generate-home",
    response_model=RecommendationResponse
)
def generate_home(
    payload: HomeRequest,
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    result = gemini_service.generate(
        "Home",
        payload.model_dump()
    )

    save_history(
        db,
        user,
        "Home",
        payload.model_dump(),
        result
    )

    return result


@router.post(
    "/generate-party",
    response_model=RecommendationResponse
)
def generate_party(
    payload: PartyRequest,
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    result = gemini_service.generate(
        "Party",
        payload.model_dump()
    )

    save_history(
        db,
        user,
        "Party",
        payload.model_dump(),
        result
    )

    return result


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse
)
async def generate_jewelry(
    budget: float = Form(..., gt=0),
    occasion: str = Form(...),
    style: str = Form("Elegant"),
    outfit_color: str = Form(
        "Not specified"
    ),
    outfit_image: UploadFile | None = File(
        None
    ),
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG, "
                    "and WEBP images "
                    "are supported"
                )
            )

    image_bytes = (
        await outfit_image.read()
        if outfit_image
        else None
    )

    if (
        image_bytes
        and len(image_bytes) > 5 * 1024 * 1024
    ):

        raise HTTPException(
            status_code=413,
            detail="Image must be 5 MB or smaller"
        )

    payload = {
        "budget": budget,
        "occasion": occasion.strip(),
        "style": style.strip(),
        "outfit_color": outfit_color.strip()
    }

    result = gemini_service.generate(
        "Jewelry",
        payload,
        image_bytes=image_bytes
    )

    save_history(
        db,
        user,
        "Jewelry",
        payload,
        result
    )

    return result


@router.get(
    "/recommendations-details"
)
def recommendations_details(
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    row = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id
            == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .first()
    )

    if not row:

        return {
            "message":
            "No recommendations yet"
        }

    return json.loads(
        row.result_json
    )


@router.get("/history")
def history(
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id
            == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [
        {
            "id": row.id,
            "planner_type":
                row.planner_type,
            "budget":
                row.budget,
            "created_at":
                (
                    row.created_at.isoformat()
                    if row.created_at
                    else None
                ),
            "request":
                json.loads(
                    row.request_json
                ),
            "result":
                json.loads(
                    row.result_json
                )
        }
        for row in rows
    ]