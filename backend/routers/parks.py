from typing import List

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import Session, select
from models import Park, VisitorCenter
from database import engine

router = APIRouter()

@router.get("/parks", response_model=List[Park])
def get_parks():
    with Session(engine) as session:
        return session.exec(select(Park)).all()
    

@router.get("/parks/{park_id}", response_model=Park)
def get_park_by_id(
    park_id: str = Path(
        ...,
        title="Park ID",
        description="Unique string identifier for the park.",
        min_length=2,
        max_length=50,
    )
):
    with Session(engine) as session:
        park = session.get(Park, park_id)
        if not park:
            raise HTTPException(
                status_code=404,
                detail=f"Park with id '{park_id}' not found",
            )
        return park


@router.get(
    "/parks/{park_id}/visitor-centers",
    response_model=List[VisitorCenter],
)
def get_visitor_centers_by_park(
    park_id: str = Path(
        ...,
        title="Park ID",
        description="Unique string identifier for the park.",
        min_length=2,
        max_length=50,
    )
):
    with Session(engine) as session:
        park = session.get(Park, park_id)
        if not park:
            raise HTTPException(
                status_code=404,
                detail=f"Park with id '{park_id}' not found",
            )

        statement = select(VisitorCenter).where(
            VisitorCenter.park_id == park_id
        )
        visitor_centers = session.exec(statement).all()
        return visitor_centers