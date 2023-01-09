import sqlite3

conn = sqlite3.connect("muvi_database")
c = conn.cursor()

async def getMovie(movieId: int):
    sql = "SELECT * FROM movies WHERE movie_id = {}".format(movieId)
    c.execute(sql)
    conn.commit()
    movie = c.fetchall()

    return movie[0]