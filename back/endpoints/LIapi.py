from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DeployableLI.back.database.models import TechTable  # Assuming you have a TechTable model

app = FastAPI()

# Database setup (assuming SQLite for simplicity)
DATABASE_URL = 'sqlite:///../app.db'  # Adjust the path as needed
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.get("/api/db/{terms}")
def db_call(terms: str):
    # Create a new session
    db = SessionLocal()
    try:
        # Query the database
        tech_data = db.query(TechTable).filter_by(term=terms).all()

        # Convert data to a format that can be returned as JSON
        result = {tech.skills: tech.counts for tech in tech_data}
        return result
    finally:
        db.close()
