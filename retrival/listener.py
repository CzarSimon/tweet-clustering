import tweepy
import sys
import json
import re
sys.path.append("..")
from database import manager as db
import api

class TweetListener(tweepy.StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if ((tweet["lang"]) and (tweet["lang"] == "en")):
            text = tweet["text"]
            db.insert_tweet(tweet["id"], text, tweet["user"]["followers_count"])
            print "Tweet: " + text.encode('utf8')
        pass

    def on_error(self, error):
        print error

def _remove_url(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

def main():
    stream_listener = TweetListener()
    stream = tweepy.Stream(auth=api.get_api().auth, listener=stream_listener)
    stream.filter(track=['Accenture', '$ACN', '#ACN'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt, e:
        print e
        print "There are " + str(len(db.get_tweets())) + " tweets in the database"
