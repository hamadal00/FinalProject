from typing import List

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import Session, select
from models import Activity
from database import engine

router = APIRouter()

@router.get("/activities", response_model=List[Activity])
def get_activities():
    with Session(engine) as session:
        return session.exec(select(Activity)).all()
    
    
@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity_by_id(
    activity_id: int = Path(
        ...,
        title="Activity ID",
        description="Internal numeric ID of the activity (must be positive).",
        gt=0,
    )
):
    with Session(engine) as session:
        activity = session.get(Activity, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity


@router.get("/parks/{park_id}/activities", response_model=List[Activity])
def get_activities_for_park(
    park_id: str = Path(
        ...,
        title="Park ID",
        description="String ID of the park, as stored in the park.id column.",
        min_length=2,
        max_length=50,
    )
):
    with Session(engine) as session:
        statement = select(Activity).where(Activity.park_id == park_id)
        activities = session.exec(statement).all()
        if not activities:
            raise HTTPException(
                status_code=404,
                detail=f"No activities found for park_id='{park_id}'",
            )
        return activities