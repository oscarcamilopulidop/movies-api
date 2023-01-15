from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My app with fastapi"
app.version = "0.0.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'action'    
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2022,
        'rating': 7.8,
        'category': 'action'    
    }  
]

@app.get('/',tags=["home"])
def message():
    return HTMLResponse("<h1>hello<h1/>")

@app.get('/movies',tags=["movies"])
def get_movies():
    return movies

@app.get('/movies/{id}',tags=["movies"])
def get_movie(id:int):
    for item in movies:
        if item['id'] == id:
            return item


def valid_querie(year:int,category:str,movie:dict):
    return movie['category'] == category and movie['year'] == year

@app.get('/movies/', tags=["movies"]) # query parameters
def get_movies_by_query(category:str,year:int=None):
    if year is None:
        return [movie for movie in movies if movie['category'] == category]
    else:
        return [movie for movie in movies if valid_querie(year,category,movie)]
    