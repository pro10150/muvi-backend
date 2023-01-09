import sqlite3

conn = sqlite3.connect("../muvi_database")

c = conn.cursor()

def getMovie(movieId: int):
    c.execute("SELECT * FROM movies WHERE movie_id IS {movieId}")