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

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM movies
                WHERE id = :id
            """),
            {"id": movie_id}
        )

        movie = result.fetchone()

        if movie is None:
            return {"message": "Movie not found"}

        return dict(movie._mapping)

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE movies
                SET title = :title,
                    genre = :genre
                WHERE id = :id
            """),
            {
                "id": movie_id,
                "title": movie.title,
                "genre": movie.genre
            }
        )

        if result.rowcount == 0:
            return {"message": "Movie not found"}

    return {"message": "Movie updated successfully"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                DELETE FROM movies
                WHERE id = :id
            """),
            {"id": movie_id}
        )

        if result.rowcount == 0:
            return {"message": "Movie not found"}

    return {"message": "Movie deleted successfully"}
