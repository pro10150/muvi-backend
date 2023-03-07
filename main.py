from typing import Union
from fastapi import FastAPI
import DBManager as db
from serpapi import GoogleSearch
import item

#init app
app = FastAPI()

#setup
serpapiKey = "1bcc076b08b97c82a4589d6d7c4ecb0d91faeb2254f1e91c9d5221ccf2345ff6"

def createParams(term: str):
    return {
        "q": term,
        "tbm": "isch",
        "ijn": "0",
        "api_key": serpapiKey
    }
#api
# get movie from movie_id
@app.get("/movie/{movieId}")
async def get_movie(movieId: int):
    movie = await db.getMovie(movieId=movieId)

    search = GoogleSearch(createParams(term=movie[17]))
    results = search.get_dict()

    return {
        "id": movie[0], 
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
        "vote_count": movie[19],
        "image_results": results["images_results"]
    }

# search movie using keyword
@app.get("/{keyword}")
async def search_keyword(keyword: str):
    # Wait for AI
    return {"keyword": keyword}

# get cast info
@app.get("/cast/{movieId}")
async def get_cast(movieId: int):
    casts = await db.getCasts(movieId=movieId)
    return {"casts": casts}

# get actor movies ordered by popularity
@app.get("/actor/movies/{actorId}/popularity")
async def get_actor_movie(actorId: int):
    movies = await db.getActorMoviesOrderByPopularity(actorId=actorId)
    return {"movies": movies}

# get actor movies ordered by vote average
@app.get("/actor/movies/{actorId}/vote")
async def get_actor_movie(actorId: int):
    movies = await db.getActorMoviesOrderByVote(actorId=actorId)
    return {"movies": movies}

# get actor info
@app.get("/actor/{actorId}")
async def get_actor(actorId: int):
    actor = await db.getActor(actorId=actorId)
    return {"actor": actor}

# get all genres
@app.get("/genre/all")
async def get_genres():
    genres = await db.getAllGenres()
    return {"genres": genres}

# get movie genres
@app.get("/genre/{movieId}")
async def get_genre(movieId):
    genres = await db.getGenre(movieId=movieId)
    return {"genres": genres}

# get all actors
@app.get("/actor/all")
async def get_actors():
    actors = await db.getAllActors()
    return {"actors": actors}

@app.get("/collection/all")
async def get_collections():
    collections = await db.getAllCollections()
    return {"collections": collections}

# post movie
@app.post("/add/movie/")
async def create_movie(movie: item.movieItem):
    await db.addMovie(movie=movie)
    return {"status": 1}

# post cast
@app.post("/add/movie/actor")
async def create_actor_movie(cast: item.castItem):
    await db.addCast(cast=cast)
    return {"status": 1}

# post collection
@app.post("/add/collection/")
async def create_collection(collection: item.collectionItem):
    await db.addCollection(collection=collection)
    return {"status": 1}

# post movie collection

# post actor
@app.post("/add/actor")
async def create_actor(actor: item.actorItem):
    await db.addActor(actor=actor)
    return {"status: 1"}
    