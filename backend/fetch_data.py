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


def populate_if_empty(engine):
    """
    If DB is empty, fetch from NPS API and insert data.
    """
    with Session(engine) as session:
        if not db_is_empty(session):
            print("Database already has data, skipping initial fetch.")
            return
        print("Database empty — fetching data from NPS API...")

        parks_data = fetch_parks(limit=50)
        vcs_data = fetch_visitor_centers(limit=50)
        activities_data = fetch_activities(limit=50)

        # Insert parks
        for p in parks_data:
            park = Park(
                id=p.get("id"),
                fullName=p.get("fullName", ""),
                parkCode=p.get("parkCode", ""),
                description=p.get("description", ""),
                latitude=str(p.get("latitude")),
                longitude=str(p.get("longitude", "")),
                latLong=p.get("latLong", ""),
                states=p.get("states", ""),
                directionsInfo=p.get("directionsInfo", ""),
                name=p.get("name", ""),
                designation=p.get("designation", ""),
            )
            session.add(park)

        # Insert visitor centers
        for v in vcs_data:
            vc = VisitorCenter(
                id=v.get("id"),
                name=v.get("name", ""),
                parkCode=v.get("parkCode", ""),
                description=v.get("description", ""),
                latitude=str(v.get("latitude", "")),
                longitude=str(v.get("longitude", "")),
                directionsInfo=v.get("directionsInfo", ""),
            )
            session.add(vc)

        # Insert activities
        for a in activities_data:
            activity = Activity(
                id=a.get("id"),
                name=a.get("name", ""),
            )
            session.add(activity)

        session.commit()
        print("Initial data load completed.")