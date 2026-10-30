from datetime import datetime
from datetime import timezone

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


def utcnow():

    return datetime.now(
        timezone.utc
    )


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )

    recommendations: Mapped[list["RecommendationHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class RecommendationHistory(Base):

    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    planner_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    budget: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    request_json: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    result_json: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )

    user: Mapped[User] = relationship(
        back_populates="recommendations"
    )