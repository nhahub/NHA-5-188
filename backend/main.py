from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Location, ElderlyProfile, FallEvent
from .schemas import (
    LocationCreate, LocationRead,
    ProfileCreate, ProfileRead,
    EventCreate, EventRead,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="DEPI Fall Detection API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "Fall Detection API is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": False,
        "camera_enabled": False,
    }


# LOCATIONS

@app.post("/locations", response_model=LocationRead, status_code=201)
def create_location(
    data: LocationCreate,
    session: Session = Depends(get_session),
):
    location = Location(**data.model_dump())
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


@app.get("/locations", response_model=list[LocationRead])
def list_locations(session: Session = Depends(get_session)):
    return session.exec(select(Location)).all()


# PROFILES

@app.post("/profiles", response_model=ProfileRead, status_code=201)
def create_profile(
    data: ProfileCreate,
    session: Session = Depends(get_session),
):
    if session.get(Location, data.location_id) is None:
        raise HTTPException(404, "Location not found")

    profile = ElderlyProfile(**data.model_dump())
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@app.get("/profiles", response_model=list[ProfileRead])
def list_profiles(
    location_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    statement = select(ElderlyProfile)

    if location_id is not None:
        statement = statement.where(
            ElderlyProfile.location_id == location_id
        )

    return session.exec(statement).all()


# HISTORY

@app.post("/history/events", response_model=EventRead, status_code=201)
def create_event(
    data: EventCreate,
    session: Session = Depends(get_session),
):
    person = session.get(ElderlyProfile, data.person_id)

    if person is None:
        raise HTTPException(404, "Profile not found")

    event = FallEvent(
        person_id=person.id,
        location_id=person.location_id,
        event_type=data.event_type,
        confidence=data.confidence,
        source=data.source,
        alert_status=(
            "pending"
            if data.event_type == "fall_detected"
            else "not_required"
        ),
        notes=data.notes,
        occurred_at=data.occurred_at or datetime.now(timezone.utc),
    )

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.get(
    "/history/person/{person_id}",
    response_model=list[EventRead],
)
def person_history(
    person_id: int,
    session: Session = Depends(get_session),
):
    if session.get(ElderlyProfile, person_id) is None:
        raise HTTPException(404, "Profile not found")

    statement = (
        select(FallEvent)
        .where(FallEvent.person_id == person_id)
        .order_by(FallEvent.occurred_at.desc())
    )
    return session.exec(statement).all()


@app.get(
    "/history/location/{location_id}",
    response_model=list[EventRead],
)
def location_history(
    location_id: int,
    session: Session = Depends(get_session),
):
    if session.get(Location, location_id) is None:
        raise HTTPException(404, "Location not found")

    statement = (
        select(FallEvent)
        .where(FallEvent.location_id == location_id)
        .order_by(FallEvent.occurred_at.desc())
    )
    return session.exec(statement).all()