import requests
from sqlmodel import Session, select

from models import Park, VisitorCenter, Activity

API_KEY = "xH4dgqQOOpYJ5uVYcMf3o0QpiMb8GZQz9hlsxeqY"

BASE_URL = "https://developer.nps.gov/api/v1"

def db_is_empty(session: Session) -> bool:
    """
    Check if all three tables are empty.
    """
    has_park = session.exec(select(Park)).first()
    has_vc = session.exec(select(VisitorCenter)).first()
    has_activity = session.exec(select(Activity)).first()
    return not (has_park or has_vc or has_activity)

def fetch_parks(limit: int = 50):
    resp = requests.get(
        f"{BASE_URL}/parks",
        params={"limit": limit, "api_key": API_KEY},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])


def fetch_visitor_centers(limit: int = 50):
    resp = requests.get(
        f"{BASE_URL}/visitorcenters",
        params={"limit": limit, "api_key": API_KEY},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])


def fetch_activities(limit: int = 50):
    resp = requests.get(
        f"{BASE_URL}/activities",
        params={"limit": limit, "api_key": API_KEY},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])