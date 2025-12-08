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

        parks_data = fetch_parks(limit=10)
        vcs_data = fetch_visitor_centers(limit=10)

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
        session.commit()
        print("All parks saved.")
        # fetch the saved parks in order to deal with relationship
        parks_in_db = session.exec(select(Park)).all()
        parkcode_to_id = {p.parkCode: p.id for p in parks_in_db}
        parkid_set = {p.id for p in parks_in_db}

        vc_count = 0
        # Insert visitor centers
        for v in vcs_data:
            park_id = parkcode_to_id.get(v.get("parkCode", ""))
            vc = VisitorCenter(
                id=v.get("id"),
                name=v.get("name", ""),
                parkCode=v.get("parkCode", ""),
                description=v.get("description", ""),
                latitude=str(v.get("latitude", "")),
                longitude=str(v.get("longitude", "")),
                directionsInfo=v.get("directionsInfo", ""),
                park_id=park_id,
            )
            session.add(vc)
            vc_count += 1

        act_count = 0
        # Insert activities
        for p in parks_data:
            park_id = p.get("id")
            if park_id not in parkid_set:
                continue
            activities_for_park = p.get("activities", [])[:10]
            for act in activities_for_park:
                activity = Activity(
                    nps_id=act.get("id", ""),
                    name=act.get("name", ""),
                    park_id=park_id,
                )
                session.add(activity)
                act_count += 1

        session.commit()
        print(f"VisitorCenters saved: {vc_count}")
        print(f"Activities saved : {act_count}")
        print("Initial data load completed.")