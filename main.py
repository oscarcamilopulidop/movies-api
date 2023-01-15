from typing import List, Optional

from fastapi import Body, FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()
app.title = "My app with fastapi"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="My title", min_length=5, max_length=20)
    overview: str = Field(default="My overview", min_length=10, max_length=100)
    year: int = Field(default=2023, le=2023)
    rating: float = Field(default=3.0, ge=0.0, le=10)
    category: str = Field(default="My title", min_length=5, max_length=20)

    class Config:
        schema_extra = {
            "title": "my title",
            "overview": "my overview",
            "year": 2019,
            "rating": 7.8,
            "category": "action",
        }


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
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)


@app.get("/movies/{id}", tags=["movies"], status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item, status_code=200)
    return JSONResponse(content=[], status_code=404)


def valid_querie(year: int, category: str, movie: dict) -> bool:
    return movie["category"] == category and movie["year"] == year


@app.get(
    "/movies/", tags=["movies"], response_model=List[Movie], status_code=200
)  # query parameters
def get_movies_by_query(
    category: str = Query(min_length=5, max_length=15), year: int = None
) -> List[Movie]:
    if year is None:
        data = [movie for movie in movies if movie["category"] == category]
    else:
        data = [
            movie for movie in movies if valid_querie(year, category, movie)
        ]
    return JSONResponse(content=data, status_code=200)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=200)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Movie saved"}, status_code=200)


@app.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=200
)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if id == movie["id"]:
            movies.remove(movie)
            return JSONResponse(
                content={"message": "Movie updated"}, status_code=200
            )
    return JSONResponse(
        content={"message": "Movie not found"}, status_code=404
    )


@app.put(
    "/movie/{movie_id}", tags=["movies"], response_model=dict, status_code=200
)
async def put_movie(movie: Movie) -> dict:
    for movie in movies:
        if movie["id"] == movie.id:
            movie.update(movie.__dict__)
            return JSONResponse(
                content={"message": "Movie updated"}, status_code=200
            )
    return JSONResponse(
        content={"message": "Movie not found"}, status_code=404
    )
