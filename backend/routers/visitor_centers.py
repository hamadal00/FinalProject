from typing import List

from fastapi import APIRouter, HTTPException, Path
from sqlmodel import Session, select
from models import VisitorCenter
from database import engine

router = APIRouter()

@router.get("/visitor_centers", response_model=List[VisitorCenter])
def get_visitor_centers():
    with Session(engine) as session:
        return session.exec(select(VisitorCenter)).all()
    
    
@router.get(
    "/visitor_centers/{visitor_center_id}",
    response_model=VisitorCenter,
)
def get_visitor_center_by_id(
    visitor_center_id: str = Path(
        ...,
        title="Visitor Center ID",
        description="Unique string identifier of the visitor center.",
        min_length=2,
        max_length=50,
    )
):
    with Session(engine) as session:
        visitor_center = session.get(VisitorCenter, visitor_center_id)
        if not visitor_center:
            raise HTTPException(
                status_code=404,
                detail=f"Visitor center with id '{visitor_center_id}' not found",
            )
        return visitor_center