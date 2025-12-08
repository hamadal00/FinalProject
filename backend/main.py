from fastapi import FastAPI,HTTPException, Request
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from datetime import date, datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sql_file = "../database/database.db"
sqlite_url = f"sqlite:///{sql_file}"
engine = create_engine(sqlite_url, echo=True)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)