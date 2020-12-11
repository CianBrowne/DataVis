from flask import Flask, render_template, request, jsonify, make_response

from twitter_auth import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import json
import schedule
import time
import pygsheets
import pandas as pd
gc = pygsheets.authorize(client_secret='static/loadable/client_secret.json')
# Authorization code: 4/5QEVrswDi311jR5OYcmGKpj75JMzwypN2CCJ0e96ei2lAbbfLExb4bU
df = pd.DataFrame()
df2 = pd.DataFrame()

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(q=query)
        scores = []
        positive = 0
        negative = 0
        neutral = 0
        for info in tweets:
            score = analyser.polarity_scores(info.text)
            scores.append(score)
        for i in scores:
            if (i['neg'] > i['pos'] and i['neg'] > i['neu']):
                print('negative')
                positive = positive + 1
            if (i['pos'] > i['neg'] and i['pos'] > i['neu']):
                print('positive')
                negative = negative + 1
            if (i['neu'] > i['neg'] and i['neu'] > i['pos']):
                print('positive')
                neutral = neutral + 1
        pos = {
            "name": "positive",
            "y": positive,
            "drilldown": "positive"
        }
        neg = {
            "name": "negative",
            "y": negative,
            "drilldown": "negative"
        }
        neu = {
            "name" : "neutral",
            "y": neutral,
            "drilldown": "drilldown"
        }
        thisArray = [pos, neg, neu]
        highcharts = []
        for i in thisArray:
            json.dumps(i)
            highcharts.append(i)
        chartSettings = [query]
        highcharts = [chartSettings, pos, neg, neu]
        print(highcharts)
        return render_template('results.html', thisArray=highcharts)
    else:
        print("not working")
        return render_template('index.html')

@app.route("/test/", methods=['POST'])
def testPrint():
    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(q=query)
        scores = []
        positive = 0
        negative = 0
        neutral = 0
        print("Working")
        for info in tweets:
            score = analyser.polarity_scores(info.text)
            scores.append(score)
        for i in scores:
            if (i['neg'] > i['pos']):
                print('negative')
                positive = positive + 1
            if (i['pos'] > i['neg']):
                print('positive')
                negative = negative + 1
        pos = {
            "name": "positive",
            "y": positive,
            "drilldown": "positive"
        }
        neg = {
            "name": "negative",
            "y": negative,
            "drilldown": "negative"
        }
        thisArray = [pos, neg]
        highcharts = []
        for i in thisArray:
            json.dumps(i)
            highcharts.append(i)
        chartSettings = [query]
        highcharts = [chartSettings, pos, neg]
     #   highcharts = processTweet(query)
        print(highcharts)
        return render_template('results.html', thisArray=highcharts)
    else:
        print("not working")
        return render_template('index.html')
@app.route("/test2/", methods=['POST'])
def compareHashtag():
    if request.method == 'POST':
        query = request.form['query']
        query2 = request.form['query2']
        array1 = processTweet2(query)
        array2 = processTweet2(query2)
        array3 = processDrilldown(query)
        array4 = processDrilldown(query2)
        highcharts = [array1, array2, array3, array4]

       # prepareCSV(query, query2)
        return render_template('tweetComp.html', thisArray=highcharts)

def liveHashtag():
    if request.method == 'POST':
        query = request.form['query']
        query2 = request.form['query2']
        array1 = processTweet2(query)
        array2 = processTweet2(query2)
        highcharts = [array1, array2]
        f = open("/static/loadable/input.csv", "r")
        f.truncate()
        return render_template('tweetComp.html', thisArray=highcharts)
def liveData(query1, query2):
    schedule.every(60).seconds.do(updateCSV, query1, query2)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/prepare", methods=["POST"])
def prepareCSV():
    req = request.get_json()

    print(req)
    print(req['query1'])
    res = make_response(jsonify({"message": "JSON received"}), 200)
    # if request.method == 'POST':
    query1 = req['query1']
    query2 = req['query2']
    print(query1)
    user1 = processTweet2(query1)
    user2 = processTweet2(query2)
    name1 = query1
    name2 = query2
    user1pos = int(user1[1]['y'])
    user1neg = int(user1[2]['y'])
    user2pos = int(user2[1]['y'])
    user2neg = int(user2[2]['y'])

    # writing to csv file
    df['name'] = [name1 + ' positive sentiment', name1 + ' negative sentiment', name2 + ' positive sentiment',
                  name2 + ' negative sentiment']
    df2['y'] = [user1pos, user1neg, user2pos, user2neg]

    sh = gc.open('testing spreadsheet')

    wks = sh[0]
    wks.set_dataframe(df, (1, 1))
    wks.set_dataframe(df2, (1, 2))
    return res
    #

@app.route("/updateCSV", methods=["POST"])
def updateCSV():
    req = request.get_json()

    print(req)
    print(req['query1'])
    res = make_response(jsonify({"message": "JSON received"}), 200)
    # if request.method == 'POST':
    query1 = req['query1']
    query2 = req['query2']
    sh = gc.open('testing spreadsheet')
    wks = sh[0]
    user1 = processTweet2(query1)
    user2 = processTweet2(query2)

    name1 = query1
    name2 = query2
    user1pos = int(user1[1]['y'] + int(wks.get_value('B2')))
    user1neg = int(user1[2]['y'] + int(wks.get_value('B3')))
    user2pos = int(user2[1]['y'] + int(wks.get_value('B4')))
    user2neg = int(user2[2]['y'] + int(wks.get_value('B5')))

    df['name'] = [name1 + ' positive sentiment', name1 + ' negative sentiment', name2 + ' positive sentiment',
                  name2 + ' negative sentiment']
    df2['y'] = [user1pos, user1neg, user2pos, user2neg]
    wks.set_dataframe(df, (1, 1))
    wks.set_dataframe(df2, (1, 2))
    return res



def processTweet(query):
    tweets = api.search(q=query)
    scores = []
    positive = 0
    negative = 0
    neutral = 0
    for info in tweets:
        score = analyser.polarity_scores(info.text)
        scores.append(score)
    for i in scores:
        if (i['neg'] > i['pos'] and i['neg'] > i['neu']):
           # print('negative')
            positive = positive + 1
        if (i['pos'] > i['neg'] and i['pos'] > i['neu']):
           # print('positive')
            negative = negative + 1
        if (i['neu'] > i['neg'] and i['neu'] > i['pos']):
           # print('positive')
            neutral = neutral + 1
    pos = {
        "name": "positive",
        "y": positive,
        "drilldown": "positive"
    }
    neg = {
        "name": "negative",
        "y": negative,
        "drilldown": "negative"
    }
    neu = {
        "name": "neutral",
        "y": neutral,
        "drilldown": "drilldown"
    }
    thisArray = [pos, neg, neu]
    highcharts = []
    for i in thisArray:
        json.dumps(i)
        highcharts.append(i)
    chartSettings = [query]
    highcharts = [chartSettings, pos, neg, neu]
   # print("test")
    return highcharts
def processDrilldown(query):
    tweets = api.search(q=query)
    drilldownID = query
    followers = 0
    retweets = 0
    for info in tweets:
        print(info.user.name)
        print(info.user.followers_count)
        followers = followers + int(info.user.followers_count)
        retweets = retweets + int(info.retweet_count)

    json1 = {
        "name": "Retweets",
        "drilldown": drilldownID,
        "y": retweets
    }
    json2 = {
        "name": "Followers",
        "drilldown": drilldownID,
        "y": followers
    }

    thisArray = [json1, json2]
    highcharts = []
    for i in thisArray:
        json.dumps(i)
        highcharts.append(i)
    chartSettings = [query]
    highcharts = [chartSettings, json1, json2]
    return highcharts
def processTweet2(query):
    tweets = api.search(q=query)
    scores = []
    positive = 0
    negative = 0
    neutral = 0
    for info in tweets:
        #tweet._json  possible new issue, use this instead of .text if it throws and error
        #tweet._json['text']/['entities']
        score = analyser.polarity_scores(info.text)
        scores.append(score)
    for i in scores:
        if (i['neg'] > i['pos']):
            positive = positive + 1
        if (i['pos'] > i['neg']):
            negative = negative + 1
    pos = {
        "name": "positive",
        "y": positive,
        "drilldown": query
    }
    neg = {
        "name": "negative",
        "y": negative,
        "drilldown": query
    }

    thisArray = [pos, neg]
    highcharts = []
    for i in thisArray:
        json.dumps(i)
        highcharts.append(i)
    chartSettings = [query]
    highcharts = [chartSettings, pos, neg]
    print("test")
    return highcharts
if __name__ == '__main__':
    app.run()
