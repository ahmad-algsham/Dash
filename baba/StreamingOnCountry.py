from tweepy import Stream, OAuthHandler, api, API
from tweepy.streaming import StreamListener
from textblob import TextBlob
from sheet import kays_twitter   # contain keys access
import json
import sqlite3

conn = sqlite3.connect('gulfstate.db')
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


auth = OAuthHandler(kays_twitter.consumer_key, kays_twitter.consumer_secret)
auth.set_access_token(kays_twitter.access_key, kays_twitter.access_secret)

twitterStream = Stream(auth,listener())
# extract top trend
api = API(auth)
result_SA = api.trends_place(23424938)

for trend in result_SA[0]["trends"][:1]:
    print(trend['name'])
    SA = trend['name']

print(SA)
twitterStream.filter(track=[SA])