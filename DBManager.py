import sqlite3
from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
import item
import random
from fastapi_login.exceptions import InvalidCredentialsException
import math
import yake


def createParams(term: str):
    return {
        "q": term,
        "tbm": "isch",
        "ijn": "0",
        "api_key": serpapiKey
    }

class Status:
    success = "success"
    fail = "fail"


conn = sqlite3.connect("muvi_database")
c = conn.cursor()

def getMovieForRecommendation():
    sql = """SELECT movies.movie_id, original_title, group_concat(name) as genres, overview, popularity
            FROM movies 
            LEFT JOIN movieGenres 
            ON movies.movie_id = movieGenres.movie_id
            LEFT JOIN genres
            ON movieGenres.genre_id = genres.id
            GROUP BY movies.movie_id"""
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []

    moviesDict = [{
                "movie_id": movie[0], 
                "original_title": movie[1], 
                "genres": movie[2],
                "overview": movie[3], 
                "popularity": movie[4], 
            } for movie in movies]

    return moviesDict

async def getAdmin(user: str):
    sql = "SELECT * FROM users WHERE user = '{}'".format(user)
    c.execute(sql)
    conn.commit()
    users = c.fetchall()

    if len(users) < 1:
        raise InvalidCredentialsException
    else:
        user = {
            'user': users[0][1],
            'password': users[0][2]
        }
        return user

async def getMovie(movieId: int, isGoogleSearch: bool):
    sql = "SELECT * FROM movies LEFT JOIN collections ON movies.belongs_to_collection = collection_id WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    extractor = yake.KeywordExtractor(n=1, top=5)

    for movie in movies:

        if movie[9] != None:
            print("keyword:")
            keywords = extractor.extract_keywords(movie[9])
        else:
            keywords = [[movie[17], 0.00]]

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
                "image": movie[20],
                "collection_name": movie[23],
                "keywords": keywords
                }
        moviesDict.append(movieDict)
        

    return moviesDict

async def getCollectionMovie(id):
    sql = 'SELECT * FROM movies WHERE belongs_to_collection = {}'.format(id)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    for movie in movies:

        movieDict = {
                "id": movie[0], 
                "movie_id": movie[5], 
                "original_title": movie[8], 
                "overview": movie[9], 
                "poster_path": movie[11], 
                "release_date": movie[12], 
                "runtime": movie[14], 
                "title": movie[17], 
                "image": movie[20],
        }
        moviesDict.append(movieDict)
    return moviesDict
    
async def getSearchMovie(movies: list):
    t = tuple(movies)
    sql = "SELECT * FROM movies WHERE movie_id IN {}".format(t)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    for movie in movies:

        movieDict = {
                "id": movie[0], 
                "movie_id": movie[5], 
                "original_title": movie[8], 
                "overview": movie[9], 
                "poster_path": movie[11], 
                "release_date": movie[12], 
                "runtime": movie[14], 
                "title": movie[17], 
                "image": movie[20],
        }
        moviesDict.append(movieDict)
    return moviesDict


async def getCasts(movieId: int, isGoogleSearch: bool):
    sql = "SELECT * FROM casts INNER JOIN actors ON casts.actor_id = actors.id INNER JOIN gender_desc ON actors.gender = gender_desc.id WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()
    casts = c.fetchall()
    castsDict = []
    for cast in casts:
            name = cast[9] + cast[10] + cast[11]
            castDict = {
                "id": cast[0],
                "movie_id": cast[1],
                "cast_id": cast[2],
                "character": cast[3],
                "credit_id": cast[4],
                "actor_id": cast[5],
                "order": cast[6],
                "gender": cast[8],
                "name": name,
                "gender_desc": cast[10],
                "profile_path": cast[12]
                }
            castsDict.append(castDict)

    return castsDict

async def getActorMoviesOrderByVote(actorId: int, isGoogleSearch: bool):
    sql = "SELECT * FROM movies WHERE movie_id IN ( SELECT movie_id FROM casts WHERE actor_id = {}) ORDER BY vote_average DESC".format(actorId)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    for movie in movies:
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
                    "movie": movie[20]
                }
        moviesDict.append(movieDict)

    return moviesDict

async def getActorMoviesOrderByPopularity(actorId: int, isGoogleSearch: bool):
    sql = "SELECT * FROM movies WHERE movie_id IN ( SELECT movie_id FROM casts WHERE actor_id = {}) ORDER BY popularity DESC".format(actorId)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []
    for movie in movies:
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
                    "movie": movie[20]
                }
        moviesDict.append(movieDict)

    return moviesDict

async def getActor(actorId: int, isGoogleSearch: bool):
    sql = "SELECT * FROM actors INNER JOIN gender_desc ON actors.gender = gender_desc.id WHERE actors.id = {}".format(actorId)
    c.execute(sql)
    conn.commit()
    actors = c.fetchall()
    actorsDict = []
    for actor in actors:
            actorDict = {
                "id": actor[0],
                "gender": actor[1],
                "firstName": actor[2],
                "middleName": actor[3],
                "familyName": actor[4],
                "profile_path": actor[5],
                "image": actor[6],
                "birthday": actor[7],
                "gender_desc": actor[9]
            }
            actorsDict.append(actorDict)

    return actorsDict   
    

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
        print(genre)
        genreDict = {
            "id": genre[2],
            "name": genre[4]
        }
        genresDict.append(genreDict)

    return genresDict

async def getAllActors(page: int, size: int):
    offset = (page - 1) * size
    sql = "SELECT * FROM actors LIMIT " + str(size) + " OFFSET " + str(offset)
    c.execute(sql)
    conn.commit()
    actors = c.fetchall()
    actorsDict = []

    for actor in actors:
        actorDict = {
            "id": actor[0],
            "gender": actor[1],
            "firstName": actor[2],
            "middleName": actor[3],
            "familyName": actor[4],
            "profile_path": actor[5],
            "image": actor[6],
            "birthday": actor[7]
        }
        actorsDict.append(actorDict)

    return actorsDict

async def getActorByKeyword(keyword: str):
    sql = "SELECT * FROM actors WHERE firstName LIKE '%{}%' or lastName LIKE '%{}%'".format(keyword)
    c.execute(sql)
    conn.commit()
    actors = c.fetchall()
    actorsDict = []

    for actor in actors:
        actorDict = {
            "id": actor[0],
            "gender": actor[1],
            "firstName": actor[2],
            "middleName": actor[3],
            "familyName": actor[4],
            "profile_path": actor[5],
            "image": actor[6],
            "birthday": actor[7]
        }
        actorsDict.append(actorDict)

    return actorsDict

async def getActorCount(size: int):
    sql = "SELECT COUNT(*) FROM actors"
    c.execute(sql)
    conn.commit()
    count = c.fetchall()
    total_page = math.ceil(count[0][0]/size)

    return {
        "count": count[0][0],
        "total_page": total_page
    }

async def getAllMovies(page: int, size: int=30):
    offset = (page - 1) * size 
    sql = "SELECT * FROM movies LIMIT " + str(size) + " OFFSET " + str(offset)
    c.execute(sql)
    conn.commit()
    movies = c.fetchall()
    moviesDict = []

    for movie in movies:
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
            "image": movie[20]

        }
        moviesDict.append(movieDict)

    return moviesDict

async def getMovieCount(size: int):
    sql = "SELECT COUNT(*) FROM movies"
    c.execute(sql)
    conn.commit()
    count = c.fetchall()
    total_page = math.ceil(count[0][0]/size)

    return {
        "count": count[0][0],
        "total_page": total_page
    }

async def getAllGenders():
    sql = "SELECT * FROM gender_desc WHERE id IS NOT 0"
    c.execute(sql)
    conn.commit()
    genders = c.fetchall()
    gendersDict = []

    for gender in genders:
        genderDict = {
            "id": gender[0],
            "description": gender[1]
        }
        gendersDict.append(genderDict)

    return gendersDict

async def getAllCollections(page: int, size: int):
    offset = (page - 1) * size
    sql = "SELECT * FROM collections LIMIT " + str(size) + " OFFSET " + str(offset)
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

async def getCollectionCount(size):
    sql = "SELECT COUNT(*) FROM collections"
    c.execute(sql)
    conn.commit()
    count = c.fetchall()
    total_page = math.ceil(count[0][0]/size)

    return {
        "count": count[0][0],
        "total_page": total_page
    }

async def getCollectionByKeyword(keyword: str):
    sql = "SELECT * FROM collections WHERE name LIKE '%{}%'".format(keyword)
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

async def getCollection(collectionId: int):
    sql = "SELECT * FROM collections WHERE collection_id = {}".format(collectionId)
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
    sql = "INSERT INTO movies (belongs_to_collection, movie_id, overview, popularity, release_date, runtime, title, vote_average, vote_count, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (movie.collection, movie_id, movie.overview, 0, movie.release_date, movie.runtime, movie.title, 0, 0, movie.image)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM movies WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        movies = c.fetchall()
        moviesDict = []

        for movie in movies:
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
                "image": movie[20]
            }
            moviesDict.append(movieDict)

        return moviesDict

async def addCast(cast: item.castItem):
    cast_id = random.randint(0, 99999999)
    credit_id = random.randint(0, 99999999)
    sql = "INSERT INTO casts (movie_id, cast_id, character, credit_id, actor_id, order_number) VALUES (?, ?, ?, ?, ?, ?)"
    values = (cast.movie_id, cast_id, cast.character, credit_id, cast.actor_id, cast.order)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM casts WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        casts = c.fetchall()
        castsDict = []

        for cast in casts:
            castDict = {
                "id": cast[0],
                "movie_id": cast[1],
                "cast_id": cast[2],
                "character": cast[3],
                "credit_id": cast[4],
                "actor_id": cast[5],
                "order": cast[6]
            }
            castsDict.append(castDict)

        return castsDict

async def addCollection(collection: item.collectionItem):
    collection_id = random.randint(0, 99999999)
    sql = "INSERT INTO collections (collection_id, name) VALUES (?, ?)"
    values = (collection_id, collection.name)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM collections WHERE id = {}".format(c.lastrowid)
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

async def addActor(actor: item.actorItem):
    sql = "INSERT INTO actors (gender, firstName, middleName, familyName, profile_path, image, birthday) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (actor.gender, actor.firstName, actor.middleName, actor.familyName, "", actor.image, actor.birthday)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM actors WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        actors = c.fetchall()
        actorsDict = []

        for actor in actors:
            actorDict = {
                "id": actor[0],
                "gender": actor[1],
                "firstName": actor[2],
                "middleName": actor[3],
                "familyName": actor[4],
                "profile_path": actor[5],
                "image": actor[6],
                "birthday": actor[7]
            }
            actorsDict.append(actorDict)

        return actorsDict
    
async def addMovieGenre(movieGenre: item.movieGenreItem):
    sql = "INSERT INTO movieGenres (movie_id, genre_id) VALUES (?, ?)"
    values = (movieGenre.movie_id, movieGenre.genre_id)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM movieGenres WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        movieGenres = c.fetchall()
        movieGenresDict = []

        for movieGenre in movieGenres:
            movieGenreDict = {
                "id": movieGenre[0],
                "movie_id": movieGenre[1],
                "genre_id": movieGenre[2],
            }
            movieGenresDict.append(movieGenreDict)

        return movieGenresDict

async def editActor(actorId: int, actor: item.actorItem):
    sql = "UPDATE actors SET gender = ?, firstName = ?, middleName = ?, familyName = ?, image = ?, birthday = ? WHERE id = ?"
    values = (actor.gender, actor.firstName, actor.middleName, actor.familyName, actor.image, actor.birthday, actorId)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM actors WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        actors = c.fetchall()
        actorsDict = []

        for actor in actors:
            actorDict = {
                "id": actor[0],
                "gender": actor[1],
                "firstName": actor[2],
                "middleName": actor[3],
                "familyName": actor[4],
                "profile_path": actor[5],
                "image": actor[6],
                "birthday": actor[7]
            }
            actorsDict.append(actorDict)

        return actorsDict
    
async def editMovie(movieId: int, movie: item.movieItem):
    sql = "UPDATE movies SET title = ?, runtime = ?, release_date = ?, belongs_to_collection = ?, overview = ?, image = ? WHERE movie_id = ?"
    values = (movie.title, movie.runtime, movie.release_date, movie.collection, movie.overview, movie.image, movieId)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM movies WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        movies = c.fetchall()
        moviesDict = []

        for movie in movies:
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
                "image": movie[20]
            }
            moviesDict.append(movieDict)

        return moviesDict
    
async def editCollection(collectionId: int, collection: item.collectionItem):
    sql = "UPDATE collections SET name = ? WHERE collection_id = ?"
    values = (collection.name, collectionId)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM collections WHERE id = {}".format(c.lastrowid)
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
    
async def editCast(castId: int, cast: item.castItem):
    sql = "UPDATE casts SET character = ? WHERE cast_id = ?"
    values = (cast.character, castId)
    c.execute(sql, values)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        assert c.lastrowid is not None
        sql = "SELECT * FROM casts WHERE id = {}".format(c.lastrowid)
        c.execute(sql)
        conn.commit()
        casts = c.fetchall()
        castsDict = []

        for cast in casts:
            castDict = {
                "id": cast[0],
                "movie_id": cast[1],
                "cast_id": cast[2],
                "character": cast[3],
                "credit_id": cast[4],
                "actor_id": cast[5],
                "order": cast[6]
            }
            castsDict.append(castDict)

        return castsDict

async def deleteActor(actorId: int):
    sql = "DELETE FROM actors WHERE id = {}".format(actorId)
    c.execute(sql)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else: 
        return Status.success
    
async def deleteMovie(movieId: int):
    sql = "DELETE FROM movies WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else: 
        return Status.success
    
async def deleteCollection(collectionId: int):
    sql = "DELETE FROM collections WHERE collection_id = {}".format(collectionId)
    c.execute(sql)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        return Status.success
    
async def deleteCast(castId: int):
    sql = "DELETE FROM casts WHERE cast_id = {}".format(castId)
    c.execute(sql)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        return Status.success
    
async def deleteMovieGenre(movieGenreId: int):
    sql = "DELETE FROM movieGenres WHERE id = {}".format(movieGenreId)
    c.execute(sql)
    conn.commit()

    if c.rowcount < 1:
        return Status.fail
    else:
        return Status.success