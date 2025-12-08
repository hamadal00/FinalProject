from datetime import date
from typing import Optional, List

from sqlmodel import Field, SQLModel

class Park(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    fullName: str
    parkCode: str
    description: str
    latitude: str
    longitude: str
    latLong: str
    states: str
    directionsInfo: str
    name: str
    designation: str

class VisitorCenter(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    parkCode: str
    description: str
    latitude: str
    longitude: str
    directionsInfo: str

class Activity(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str