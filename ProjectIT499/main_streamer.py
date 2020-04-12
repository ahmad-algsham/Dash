"""
Streaming Tweets and Sentiment from Twitter in Python - Sentiment Analysis GUI with Dash and Python p.2
https://pythonprogramming.net/twitter-stream-sentiment-analysis-python/
"""
from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener
import sqlite3
import json
import time
from unidecode import unidecode
from sheet import kays_twitter  # contain keys access
from textblob_ar import TextBlob

conn = sqlite3.connect('twitter.db')
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
    conn.commit()


create_table()


class listener(StreamListener):

    def on_data(self, data):
        # TODO check extended tweet
        # print(data.extended_tweet.full_text)
        try:
            data = json.loads(data)

            tweet = data['text']  # assign to tweet if data less then 140 character
            if "extended_tweet" in data:   # assign to tweet if data more then 140 character and if data is tweet
                tweet = data['extended_tweet']['full_text']
            if "retweeted_status" in data:  # assign to tweet if data more then 140 character and if data is retweet
                if "extended_tweet" in data['retweeted_status']:
                    tweet = data['retweeted_status']['extended_tweet']['full_text']
                else:
                    tweet = data['retweeted_status']['text']

            time_ms = data['timestamp_ms']

            time.sleep(0.2)
            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity

            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                      (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print('type error: ', str(e))
        return True

    def on_error(self, status):
        if status.reason[0]['code'] == "420":
            print('error: ', status)


while True:
    try:
        auth = OAuthHandler(kays_twitter.consumer_key, kays_twitter.consumer_secret)
        auth.set_access_token(kays_twitter.access_key, kays_twitter.access_secret)

        twitterStream = Stream(auth, listener(), tweet_mode='extended')

        # extract top trend
        api = API(auth)
        result_SA = api.trends_place(23424938)  # location of Saudi Arabia
        for trend in result_SA[0]["trends"][:1]: SA = trend['name']

        twitterStream.filter(track=[SA], encoding='utf-8')
        # twitterStream.filter(track=["a", "e", "i", "o", "u"])

    except Exception as e:
        print('while not True: ', str(e))
        time.sleep(10)
