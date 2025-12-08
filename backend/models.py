from datetime import date
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel

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
    visitor_centers: List["VisitorCenter"] = Relationship(back_populates="park")
    activities: List["Activity"] = Relationship(back_populates="park")

class VisitorCenter(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    parkCode: str
    description: str
    latitude: str
    longitude: str
    directionsInfo: str
    park_id: Optional[str] = Field(default=None, foreign_key="park.id")
    park: Optional[Park] = Relationship(back_populates="visitor_centers")

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nps_id: str
    name: str
    park_id: Optional[str] = Field(default=None, foreign_key="park.id")
    park: Optional[Park] = Relationship(back_populates="activities")