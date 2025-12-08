from sqlmodel import create_engine

sql_file = "../database/database.db"
sqlite_url = f"sqlite:///{sql_file}"
engine = create_engine(sqlite_url, echo=True)
