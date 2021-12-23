# import files and give access to tokens and keys
import tweepy
import pandas as pd
import time
import json
import sys
import csv
from pyowm.owm import OWM
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

APIKEY = ''

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

RUNTIME = 3600    # Seconds to run code
weatherUpdateInterval = 300    # Seconds to update weather information

res = []


class StdOutListener(tweepy.Stream):
    def on_status(self, status):
        try:
            lang = status.lang
            text = atRemover(status.text)
            sentiment = analyzeSentiment(text)
            if lang == 'en' and len(text.split()) > 3 and sentiment != 'Cannot analyze':
                sent = {'Sentiment': sentiment}
            
                
                dateCreated = status.created_at
                box = [v for v in status.place.bounding_box.coordinates[0]]
                msg = {'Date': dateCreated, 'Text': text, 'Box': box}
                weatherCond = {'Status': weather_status, 'Temperature': temperature, 'Wind': wind}
                msg.update(weatherCond)
                msg.update(sent)
                if len(msg) == 7:
                    res.append(msg)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)


def countdown(t, mgr, weatherUpdateInterval):
    global weather_status
    global temperature
    global wind
    
    for i in range(t, -1, -1):
        if (t - i) % weatherUpdateInterval == 0:
            weather = mgr.weather_at_place('New York').weather
            weather_status = weather.status
            temperature = weather.temperature('celsius')['temp']
            wind = weather.wind()['speed']

        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print()


def atRemover(text):
    words = text.split()
    while words[0][0] == '@':
        words.pop(0)
    return ' '.join(words)


def analyzeSentiment(text):
    sentimentAnalyzerVader = SIA().polarity_scores(text)['compound']        
    sentimentAnalyzerTextBlob = TextBlob(text).sentiment[0]
    
    if sentimentAnalyzerTextBlob > 0 and sentimentAnalyzerVader > 0:
        return 'Positive'
    elif sentimentAnalyzerTextBlob < 0 and sentimentAnalyzerVader < 0:
        return 'Negative'
    return 'Cannot analyze'
        


if __name__ == "__main__":
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  threaded=True)
    
    owm = OWM(APIKEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('New York').weather
    
    countdown(RUNTIME, mgr, weatherUpdateInterval)
    stream.disconnect()

    try:
        exists = False
        with open ('tweets2.csv', 'r', encoding='utf-8') as csvfile:
            for row in csvfile:
                exists = True
                break
    except:
        exists = False
            
    with open ('tweets2.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Date','Text','Box', 'Status', 'Temperature', 'Wind', 'Sentiment'],
                                lineterminator = '\n')
        if not exists:
            writer.writeheader()
        for data in res:
            writer.writerow(data)

