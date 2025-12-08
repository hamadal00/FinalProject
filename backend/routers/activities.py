from typing import List

from fastapi import APIRouter
from sqlmodel import Session, select
from models import Activity
from database import engine

router = APIRouter()

@router.get("/activities", response_model=List[Activity])
def get_activities():
    with Session(engine) as session:
        return session.exec(select(Activity)).all()