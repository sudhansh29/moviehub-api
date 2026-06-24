from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "MovieHub API Running"}

@app.get("/movies")
def get_movies():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM movies
            ORDER BY id
            """)
        )

        movies = [dict(row._mapping) for row in result]

    return movies
