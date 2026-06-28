from fastapi import APIRouter
from sqlalchemy import text
from database import engine
from schemas import Movie

router = APIRouter()

@router.get("/movies")
def get_movies():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM movies
            """)
        )

        movies = [dict(row._mapping) for row in result]

    return movies

@router.post("/movies")
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

@router.get("/movies/{movie_id}")
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

@router.put("/movies/{movie_id}")
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

@router.delete("/movies/{movie_id}")
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
