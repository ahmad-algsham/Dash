import time
from tweepy import Stream, OAuthHandler, api, API
from tweepy.streaming import StreamListener
from textblob_ar import TextBlob
from sheet import kays_twitter  # contain keys access
import json

import sqlite3
# create DataBase
conn = sqlite3.connect('gulfstate.db')
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
    conn.commit()


create_table()


# # # # TWITTER STREAMING # # # #
class listener(StreamListener):

    def on_data(self, data):
        # print(data.extended_tweet.full_text)
        try:
            data = json.loads(data)     # load data to json format
            tweet = data['text']  # assign to tweet if data less then 140 character
            if "extended_tweet" in data:  # assign to tweet if data more then 140 character and if data is tweet
                tweet = data['extended_tweet']['full_text']
            if "retweeted_status" in data:  # assign to tweet if data more then 140 character and if data is retweet
                tweet = data['retweeted_status']['extended_tweet']['full_text']

            time_ms = data['timestamp_ms']

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
            time.sleep(5)


while True:
    print('while')
    try:
        print('auth')
        auth = OAuthHandler(kays_twitter.consumer_key, kays_twitter.consumer_secret)  # for authenticate
        auth.set_access_token(kays_twitter.access_key, kays_twitter.access_secret)    # set authentication
        print('Stream')
        twitterStream = Stream(auth, listener(), tweet_mode='extended')   # assign streaming

        # extract top trend
        api = API(auth)
        result_SA = api.trends_place(23424938)   # location of Saudi Arabia

        for trend in result_SA[0]["trends"][:1]:
            print(trend['name'])
            SA = trend['name']
        print(SA)
        twitterStream.filter(track=[SA], languages='ar')
    except Exception as e:
        print(str(e))
        time.sleep(5)
