import sqlite3

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
            "profile_path": cast[10]
            }
        castsDict.append(castDict)

    return castsDict

async def getActorMoviesOrderByVote(actorId: int):
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
            "vote_count": movie[19]
        }
        moviesDict.append(movieDict)

    return moviesDict

async def getActorMoviesOrderByPopularity(actorId: int):
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
            "vote_count": movie[19]
        }
        moviesDict.append(movieDict)

    return moviesDict

async def getActor(actorId: int):
    sql = "SELECT * FROM actors WHERE id = {}".format(actorId)
    c.execute(sql)
    conn.commit()
    actor = c.fetchall()
    actor = actor[0]
    actorDict = {
        "id": actor[0],
        "gender": actor[1],
        "name": actor[2],
        "profile_path": actor[3]
    }

    return actorDict