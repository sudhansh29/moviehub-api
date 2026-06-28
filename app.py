from fastapi import FastAPI
from database import engine
from sqlalchemy import  text
from schemas import Movie as MovieSchema
from models import Movie as MovieModel
import os
from routers.movies import router as movie_router
from routers.users import router as user_router

app = FastAPI()

app.include_router(movie_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "MovieHub API Running"}

