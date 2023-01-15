from typing import Optional

from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
app.title = "My app with fastapi"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: str
    rating: str
    category: str


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora",
        "year": 2009,
        "rating": 7.8,
        "category": "action",
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora vi...",
        "year": 2022,
        "rating": 7.8,
        "category": "action",
    },
]


@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>hello<h1/>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item


def valid_querie(year: int, category: str, movie: dict):
    return movie["category"] == category and movie["year"] == year


@app.get("/movies/", tags=["movies"])  # query parameters
def get_movies_by_query(category: str, year: int = None):
    if year is None:
        return [movie for movie in movies if movie["category"] == category]
    else:
        return [
            movie for movie in movies if valid_querie(year, category, movie)
        ]


@app.post("/movies", tags=["movies"])
def create_movie(movie: Movie):
    movies.append(movie)


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for movie in movies:
        if id == movie["id"]:
            movies.remove(movie)
            return {"erased"}


@app.put("/movie/{movie_id}", tags=["movies"])
async def put_movie(movie: Movie):
    for movie in movies:
        if movie["id"] == movie.id:
            movie.update(movie.__dict__)
