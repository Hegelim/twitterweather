import tweepy
import pandas as pd
import time
import json
import sys
from textblob import TextBlob
import logging
import os

TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

RUNTIME = 10

res = []


class StdOutListener(tweepy.Stream):
    def on_data(self, data):
        try:
            msg = json.loads(data)
            res.append(msg)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)


def countdown(t):
    for i in range(t, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print()


def update_tweets(timer=10):
    """Update tweets. """
    logging.info("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages=['en'],
                  threaded=True)
    countdown(timer)
    stream.disconnect()
    df = pd.json_normalize(res).loc[:, ["created_at", "id", "text"]]
    df[['polarity', 'subjectivity']] = df['text'].apply(lambda x: pd.Series(TextBlob(x).sentiment))
    df["inferred"] = pd.to_datetime(df["created_at"], infer_datetime_format=True)
    df["Time"] = df["inferred"].dt.tz_localize("utc").dt.tz_convert("US/Eastern").dt.tz_localize(None)
    df = df.rename(columns={"id": "Id",
                            "text": "Text",
                            "polarity": "Polarity",
                            "subjectivity": "Subjectivity"})
    df = df.loc[:, ["Time", "Id", "Text", "Polarity", "Subjectivity"]]
    workdir = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(workdir, "data/tweet_with_sentiment_local.csv")
    df.to_csv(datadir)


def get_all_tweets(timer=10):
    """Get all tweets without slicing in a given timeframe. """
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages=['en'],
                  threaded=True)
    countdown(timer)
    stream.disconnect()
    df = pd.json_normalize(res)
    df.to_csv("tweetsexample.csv")
