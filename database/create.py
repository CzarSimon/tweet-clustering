import sqlite3 as db
import sys

def _create_schema():
    print "Creating schema in tweet db sqlite version: " + db.sqlite_version
    try:
        conn = db.connect("../tweet.db")
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Tweets")
        cur.execute("CREATE TABLE Tweets(Id INT, tweet TEXT, followers INT)")
        conn.commit()
    except db.Error, e:
        print "Well that didn't work..."
        print e
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def _main():
    _create_schema()

if __name__ == '__main__':
    _main()
