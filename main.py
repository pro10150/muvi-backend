from typing import Union
from fastapi import FastAPI
import DBManager as db

#init app
app = FastAPI()

#setup

#api
# get movie from movie_id
@app.get("/movie/{movieId}")
async def get_movie(movieId: int):
    movie = await db.getMovie(movieId=movieId)
    return {"id": movie[0], 
            "adult": movie[1], 
            "belongs_to_collection": movie[2], 
            "budget": movie[3], 
            "homepage": movie[4], 
            "movie_id": movie[5], 
            "imdb_id": movie[6], 
            "original_language": movie[7], 
            "original_title": movie[8], 
            "overview": movie[9], 
            "popularity": movie[10], 
            "poster_path": movie[11], 
            "release_date": movie[12], 
            "revenue": movie[13], 
            "runtime": movie[14], 
            "status": movie[15], 
            "tagline" : movie[16], 
            "title": movie[17], 
            "vote_average": movie[18], 
            "vote_count": movie[19]}

# search movie using keyword
@app.get("/{keyword}")
async def search_keyword(keyword: str):
    # Wait for AI
    return {"keyword": keyword}

# get cast info
@app.get()