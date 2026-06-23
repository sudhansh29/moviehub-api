from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = "postgresql://postgres:Sudh123@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Welcome to MovieHub API"}

@app.get("/movies")
def get_movies():

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT *
            FROM movies
            ORDER BY id
        """))

        movies = [dict(row._mapping) for row in result]

    return movies