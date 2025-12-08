from typing import List

from fastapi import APIRouter
from sqlmodel import Session, select
from models import Park
from database import engine

router = APIRouter()

@router.get("/parks", response_model=List[Park])
def get_parks():
    with Session(engine) as session:
        return session.exec(select(Park)).all()