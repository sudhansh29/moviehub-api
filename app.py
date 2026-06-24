from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

class Movie(BaseModel):
    title: str
    genre: str

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

@app.post("/movies")
def add_movie(movie: Movie):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO movies(title, genre)
                VALUES (:title, :genre)
            """),
            {
                "title": movie.title,
                "genre": movie.genre
            }
        )

    return {"message": "Movie added successfully"}
