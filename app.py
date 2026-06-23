from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "MovieHub API Running"}

@app.get("/movies")
def movies():
    return [
        {"id": 1, "title": "Interstellar"},
        {"id": 2, "title": "Inception"},
        {"id": 3, "title": "RRR"}
    ]
