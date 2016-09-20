import sqlite3 as db
import sys

conn = db.connect("../tweet.db")

def insert_tweet(id, text, followers):
    cur = conn.cursor()
    cur.execute("INSERT INTO Tweets VALUES(?, ?, ?)", (id, text, followers))
    conn.commit()
    pass

def _get_all_tweets():
    cur = conn.cursor()
    cur.execute("SELECT id, tweet, followers FROM Tweets")
    return cur.fetchall()

def get_tweets():
    all_tweets = _get_all_tweets()
    return map(lambda row: {"id": row[0], "text": row[1], "followers": row[2]}, all_tweets)

def print_tweets():
    for tweet in _get_all_tweets():
        print tweet[1].encode('utf8')
    pass
