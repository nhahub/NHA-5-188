from datetime import datetime
from typing import Literal, Optional

from sqlmodel import SQLModel, Field

LocationType = Literal["home", "nursing_home"]
EventType = Literal["fall_detected", "no_fall", "unknown"]
EventSource = Literal["manual", "model"]


class LocationCreate(SQLModel):
    name: str = Field(min_length=1, max_length=150)
    location_type: LocationType
    address: Optional[str] = None


class LocationRead(SQLModel):
    id: int
    name: str
    location_type: str
    address: Optional[str]
    created_at: datetime


class ProfileCreate(SQLModel):
    location_id: int
    full_name: str = Field(min_length=1, max_length=150)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class ProfileRead(SQLModel):
    id: int
    location_id: int
    full_name: str
    age: Optional[int]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    face_image_path: Optional[str]
    created_at: datetime


class EventCreate(SQLModel):
    person_id: int
    event_type: EventType = "unknown"
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
    source: EventSource = "manual"
    notes: Optional[str] = None
    occurred_at: Optional[datetime] = None


class EventRead(SQLModel):
    id: int
    person_id: int
    location_id: int
    event_type: str
    confidence: Optional[float]
    source: str
    alert_status: str
    notes: Optional[str]
    occurred_at: datetime
    created_at: datetime