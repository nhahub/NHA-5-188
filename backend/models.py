from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def utc_now():
    return datetime.now(timezone.utc)


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=150)
    location_type: str = Field(index=True, max_length=30)
    address: Optional[str] = Field(default=None, max_length=300)
    created_at: datetime = Field(default_factory=utc_now)


class ElderlyProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="location.id", index=True)

    full_name: str = Field(index=True, max_length=150)
    age: Optional[int] = Field(default=None, ge=0, le=120)

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    # Face images can be added later.
    face_image_path: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)


class FallEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(
        foreign_key="elderlyprofile.id", index=True
    )
    location_id: int = Field(
        foreign_key="location.id", index=True
    )

    event_type: str = Field(default="unknown", index=True)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
    source: str = Field(default="manual", max_length=20)
    alert_status: str = Field(default="pending", max_length=20)
    notes: Optional[str] = None

    occurred_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)