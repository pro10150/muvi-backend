from typing import Union, Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import DBManager as db
import AuthManager as ath
from serpapi import GoogleSearch
import item
from fastapi.middleware.cors import CORSMiddleware
from fastapi_login import LoginManager
from datetime import timedelta
import os
import requests

#init app
app = FastAPI()

os.environ['secret-key'] = str(os.urandom(24).hex)

SECRET = os.environ.get('secret-key')

manager = LoginManager(SECRET, token_url='/login')
aiAPI = "https://muvi-backend-ai.herokuapp.com"

@manager.user_loader()
async def query_user(user_id: str):
    user = await db.getAdmin(user=user_id)
    return user

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#setup
serpapiKey = "1639863c98443e9681f070e981d21895a72d5d7cbfb77e6167ab36a968d71ad8"

class Status:
    success = "success"
    fail = "fail"

def createParams(term: str):
    return {
        "q": term,
        "tbm": "isch",
        "ijn": "0",
        "api_key": serpapiKey
    }
#api

# get movie from movie_id
@app.get("/movie/getById/{movieId}")
async def get_movie(movieId: int, isGoogleSearch: bool=True):
    movie = await db.getMovie(movieId=movieId, isGoogleSearch=isGoogleSearch)

    keywords = movie[0]["keywords"]
    keyword = ''
    print(keywords)
    for key in keywords:
        keyword = keyword + ' ' + key[0]
    
    results = requests.get("{}/search/{}".format(aiAPI, keyword))
    movies = results.json()["movies"]
    id = []
    for m in movies:
        id.append(m["id"])
    recommendations = await db.getSearchMovie(movies=id)

    filteredRecommendations = []

    collectionId = movie[0]["belongs_to_collection"]
    if collectionId != None:
        collectionMovies = await db.getCollectionMovie(id=collectionId)

        recommendations = collectionMovies + recommendations

    for recommendation in recommendations:
        if recommendation['movie_id'] != movie[0]['movie_id']:
            filteredRecommendations.append(recommendation)

    return {"movie": movie,
            "recommendation": filteredRecommendations
            }

# get all movies
@app.get("/movie/all")
async def get_all_movie(page: int=1, size: int=30):
    movies = await db.getAllMovies(page=page, size=size)
    count = await db.getMovieCount(size=size)
    return {
        "page": page,
        "size": size,
        "count": count["count"],
        "total_page": count["total_page"],
        "movies": movies
        }

# search movie using keyword
@app.get("/search/{keyword}")
async def search_keyword(keyword: str):
    results = requests.get("{}/search/{}".format(aiAPI, keyword))
    movies = results.json()["movies"]
    id = []
    for movie in movies:
        id.append(movie["id"])
    movieDetails = await db.getSearchMovie(movies=id)
    return {
        "keyword": keyword,
        "movies": movieDetails
        }

# get cast info
@app.get("/cast/getById/{movieId}")
async def get_cast(movieId: int, isGoogleSearch: bool=True):
    casts = await db.getCasts(movieId=movieId, isGoogleSearch=isGoogleSearch)
    return {"casts": casts}

# get actor movies ordered by popularity
@app.get("/actor/movies/{actorId}/popularity")
async def get_actor_movie(actorId: int, isGoogleSearch: bool=True):
    movies = await db.getActorMoviesOrderByPopularity(actorId=actorId, isGoogleSearch=isGoogleSearch)
    return {"movies": movies}

# get actor movies ordered by vote average
@app.get("/actor/movies/{actorId}/vote")
async def get_actor_movie(actorId: int, isGoogleSearch: bool=True):
    movies = await db.getActorMoviesOrderByVote(actorId=actorId, isGoogleSearch=isGoogleSearch)
    return {"movies": movies}

# get actor info
@app.get("/actor/getById/{actorId}")
async def get_actor(actorId: int, isGoogleSearch: bool=True):
    actor = await db.getActor(actorId=actorId, isGoogleSearch=isGoogleSearch)
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
async def get_actors(page: int=1, size: int=30):
    actors = await db.getAllActors(page=page, size=size)
    count = await db.getActorCount(size=size)
    return {
        "page": page,
        "size": size,
        "count": count["count"],
        "total_page": count["total_page"],
        "actors": actors
        }

# get actor by keyword
@app.get("/actor/getByKeyword/{keyword}")
async def get_actor_keyword(keyword):
    actors = await db.getActorByKeyword(keyword=keyword)
    return {
        "actors": actors
    }

# get all collections
@app.get("/collection/all")
async def get_collections(page: int=1, size: int=30):
    collections = await db.getAllCollections(page=page, size=size)
    count = await db.getCollectionCount(size=size)
    return {
        "page": page,
        "size": size,
        "count": count["count"],
        "total_page": count["total_page"],
        "collections": collections
        }

# get collection by keywords
@app.get("/collection/getByKeyword/{keyword}")
async def get_collection_by_keyword(keyword):
    collections = await db.getCollectionByKeyword(keyword=keyword)
    return {
        "collections": collections
    }

# get all genders
@app.get("/gender/all")
async def get_genders():
    genders = await db.getAllGenders()
    return {"genders": genders}

# get collection
@app.get("/collection/getById/{collectionId}")
async def get_collection(collectionId):
    collection = await db.getCollection(collectionId=collectionId)
    return {"collections": collection}

# protected

@app.get("/protected")
def protected_route(user=Depends(manager)):
    return {'user': user}

# post
# login
@app.post("/login")
async def login(user: item.loginItem):
    user = await ath.login(user=user)
    access_token = manager.create_access_token(
         data=dict(sub=user)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# post movie
@app.post("/add/movie")
# async def create_movie(movie: item.movieItem, user=Depends(manager)):
#     print(user)
#     status = await db.addMovie(movie=movie)
#     return {'user': user, "status": status}

async def create_movie(movie: item.movieItem):
    status = await db.addMovie(movie=movie)
    return {"status": status}


# post cast
@app.post("/add/cast")
# async def create_actor_movie(cast: item.castItem, user=Depends(manager)):
#     status = await db.addCast(cast=cast)
#     return {"status": status}

async def create_actor_movie(cast: item.castItem):
    status = await db.addCast(cast=cast)
    return {"status": status}

# post collection
@app.post("/add/collection")
# async def create_collection(collection: item.collectionItem, user=Depends(manager)):
#     status = await db.addCollection(collection=collection)
#     return {"status": status}

async def create_collection(collection: item.collectionItem):
    status = await db.addCollection(collection=collection)
    return {"status": status}

# post movie genre
@app.post("/add/movieGenre")
# async def create_movieGenre(movieGenre: item.movieGenreItem, user=Depends(manager)):
#     status = await db.addMovieGenre(movieGenre=movieGenre)
#     return {"status": status}

async def create_movieGenre(movieGenre: item.movieGenreItem):
    status = await db.addMovieGenre(movieGenre=movieGenre)
    return {"status": status}

# post actor
@app.post("/add/actor")
# async def create_actor(actor: item.actorItem, user=Depends(manager)):
#     status = await db.addActor(actor=actor)
#     return {"status": status}

async def create_actor(actor: item.actorItem):
    status = await db.addActor(actor=actor)
    return {"status": status}

# test
@app.get("/forTestingPurposeOnly")
async def testing():
    return {"status": "Test successfully"}

# home
@app.get("/")
async def home():
    return {"status": "This is homepage. You have successfully logged in"}

# Edit

# edit Actor
@app.put("/edit/actor")
# async def edit_actor(actorId: int, actor: item.actorItem, user=Depends(manager)):
#     status = await db.editActor(actorId=actorId, actor=actor)
#     return {"status": status}

async def edit_actor(actorId: int, actor: item.actorItem):
    status = await db.editActor(actorId=actorId, actor=actor)
    return {"status": status}

# edit Movie
@app.put("/edit/movie")
# async def edit_movie(movieId: int, movie: item.movieItem, user=Depends(manager)):
#     status = await db.editMovie(movieId= movieId, movie=movie)
#     return {"status": status}

async def edit_movie(movieId: int, movie: item.movieItem):
    status = await db.editMovie(movieId= movieId, movie=movie)
    return {"status": status}

# edit collection
@app.put("/edit/collection")
# async def edit_collection(collectionId: int, collection: item.collectionItem, user=Depends(manager)):
#     status = await db.editCollection(collectionId=collectionId, collection=collection)
#     return {"status": status}

async def edit_collection(collectionId: int, collection: item.collectionItem):
    status = await db.editCollection(collectionId=collectionId, collection=collection)
    return {"status": status}

# edit Cast
@app.put("/edit/cast")
# async def edit_cast(castId: int, cast: item.castItem, user=Depends(manager)):
#     status = await db.editCast(castId=castId, cast=cast)
#     return {"status": status}

async def edit_cast(castId: int, cast: item.castItem):
    status = await db.editCast(castId=castId, cast=cast)
    return {"status": status}

# Delete

# delete Actor
@app.delete("/delete/actor")
# async def delete_actor(actorId: int, user=Depends(manager)):
#     status = await db.deleteActor(actorId=actorId)
#     return {"status": status}
    
async def delete_actor(actorId: int):
    status = await db.deleteActor(actorId=actorId)
    return {"status": status}

# delete Movie
@app.delete("/delete/movie")
# async def delete_movie(movieId: int, user=Depends(manager)):
#     status = await db.deleteMovie(movieId=movieId)
#     return {"status": status}

async def delete_movie(movieId: int):
    status = await db.deleteMovie(movieId=movieId)
    return {"status": status}

# delete Collection
@app.delete("/delete/collection")
# async def delete_collection(collectionId: int, user=Depends(manager)):
#     status = await db.deleteCollection(collectionId=collectionId)
#     return {"status": status}

async def delete_collection(collectionId: int):
    status = await db.deleteCollection(collectionId=collectionId)
    return {"status": status}

# delete Cast
@app.delete("/delete/cast")
# async def delete_cast(castId: int, user=Depends(manager)):
#     status = await db.deleteCast(castId=castId)
#     return {"status": status}

async def delete_cast(castId: int):
    status = await db.deleteCast(castId=castId)
    return {"status": status}

# delete MovieGenre
@app.delete("/delete/movieGenre")
# async def delete_movieGenre(movieGenreId: int, user=Depends(manager)):
#     status = await db.deleteMovieGenre(movieGenreId=movieGenreId)
#     return {"status": status}

async def delete_movieGenre(movieGenreId: int):
    status = await db.deleteMovieGenre(movieGenreId=movieGenreId)
    return {"status": status}

    