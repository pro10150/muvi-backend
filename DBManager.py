import sqlite3
from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
import item
import random

#setup
serpapiKey = "1bcc076b08b97c82a4589d6d7c4ecb0d91faeb2254f1e91c9d5221ccf2345ff6"

def createParams(term: str):
    return {
        "q": term,
        "tbm": "isch",
        "ijn": "0",
        "api_key": serpapiKey
    }


conn = sqlite3.connect("muvi_database")
c = conn.cursor()

async def getMovie(movieId: int):
    sql = "SELECT * FROM movies WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()
    movie = c.fetchall()

    return movie[0]

async def getCasts(movieId: int):
    sql = "SELECT * FROM casts INNER JOIN actors ON casts.actor_id = actors.id WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()
    casts = c.fetchall()
    castsDict = []
    for cast in casts:
        search = GoogleSearch(createParams(term=cast[9]))
        result = search.get_dict()

        castDict = {
            "id": cast[0],
            "movie_id": cast[1],
            "cast_id": cast[2],
            "character": cast[3],
            "credit_id": cast[4],
            "actor_id": cast[5],
            "order": cast[6],
            "gender": cast[8],
            "name": cast[9],
            "profile_path": cast[10],
            "images_results": result["images_results"]
            }
        castsDict.append(castDict)

    return castsDict

async def getActorMoviesOrderByVote(actorId: int):
    sql = "SELECT * FROM movies WHERE movie_id IN ( SELECT movie_id FROM casts WHERE actor_id = {}) ORDER BY vote_average DESC".format(actorId)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    if len(movies) > 3:
        for i in range(5):
            movie = movies[i]
            search = GoogleSearch(createParams(term=movie[17]))
            result = search.get_dict()
            
            movieDict = {
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
                "images_results": result["images_results"]
            }
            moviesDict.append(movieDict)
    else:
        for movie in movies:
            search = GoogleSearch(createParams(term=movie[17]))
            result = search.get_dict()
            
            movieDict = {
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
                "images_results": result["images_results"]
            }
            moviesDict.append(movieDict)

    return moviesDict

async def getActorMoviesOrderByPopularity(actorId: int):
    sql = "SELECT * FROM movies WHERE movie_id IN ( SELECT movie_id FROM casts WHERE actor_id = {}) ORDER BY popularity DESC".format(actorId)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    if len(movies) > 3:
        for i in range(5):
            movie = movies[i]
            search = GoogleSearch(createParams(term=movie[17]))
            result = search.get_dict()
            
            movieDict = {
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
                "images_results": result["images_results"]
            }
            moviesDict.append(movieDict)
    else:
        for movie in movies:
            search = GoogleSearch(createParams(term=movie[17]))
            result = search.get_dict()
            
            movieDict = {
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
                "images_results": result["images_results"]
            }
            moviesDict.append(movieDict)

    return moviesDict

async def getActor(actorId: int):
    sql = "SELECT * FROM actors WHERE id = {}".format(actorId)
    c.execute(sql)
    conn.commit()
    actor = c.fetchall()
    actor = actor[0]
    search = GoogleSearch(createParams(term=actor[2]))
    result = search.get_dict()
    
    actorDict = {
        "id": actor[0],
        "gender": actor[1],
        "name": actor[2],
        "profile_path": actor[3],
        "images_results": result["images_results"]
    }

    return actorDict

async def getAllGenres():
    sql = "SELECT * FROM genres"
    c.execute(sql)
    conn.commit()
    genres = c.fetchall()
    genresDict = []

    for genre in genres:
        genreDict = {
            "id": genre[0],
            "name": genre[1]
        }
        genresDict.append(genreDict)

    return genresDict

async def getGenre(movieId):
    sql = "SELECT * FROM movieGenres INNER JOIN genres ON genres.id = movieGenres.genre_id WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()

    genres = c.fetchall()
    genresDict = []

    for genre in genres:
        genreDict = {
            "id": genre[0],
            "name": genre[1]
        }
        genresDict.append(genreDict)

    return genresDict

async def getAllActors():
    sql = "SELECT * FROM actors"
    c.execute(sql)
    conn.commit()
    actors = c.fetchall()
    actorsDict = []

    for actor in actors:
        actorDict = {
            "id": actor[0],
            "gender": actor[1],
            "name": actor[2],
            "profile_path": actor[3]
        }
        actorsDict.append(actorDict)

    return actorsDict

async def getAllCollections():
    sql = "SELECT * FROM collections"
    c.execute(sql)
    conn.commit()
    collections = c.fetchall()
    collectionsDict = []

    for collection in collections:
        collectionDict = {
            "id": collection[0],
            "collection_id": collection[1],
            "name": collection[2],
            "poster_path": collection[3],
            "backdrop_path": collection[4]
        }
        collectionsDict.append(collectionDict)

    return collectionsDict

async def addMovie(movie: item.movieItem):
    movie_id = random.randint(0, 99999999)
    sql = "INSERT INTO movies (belongs_to_collection, movie_id, overview, popularity, release_date, runtime, title, vote_average, vote_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (movie.collection, movie_id, movie.overview, 0, movie.release_date, movie.runtime, movie.title, 0, 0)
    c.execute(sql, values)
    conn.commit()

async def addCollection(collection: item.collectionItem):
    collection_id = random.randint(0, 99999999)
    sql = "INSERT INTO collections (collection_id, name) VALUES (?, ?)"
    values = (collection_id, collection.name)
    c.execute(sql, values)
    conn.commit()
