from typing import List

from fastapi import APIRouter
from sqlmodel import Session, select
from models import VisitorCenter
from database import engine

router = APIRouter()

@router.get("/visitor_centers", response_model=List[VisitorCenter])
def get_visitor_centers():
    with Session(engine) as session:
        return session.exec(select(VisitorCenter)).all()