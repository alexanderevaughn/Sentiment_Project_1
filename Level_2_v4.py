# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:16:16 2017

Purpose: To create the following analyses for a binary choice:

    1. A twitter sentiment analysis of key words, including
    the keywords' names and any newsworthy items that appear alongside them

@author: Alexander E. Vaughn

Updates:
        V1  Alexander E. Vaughn  1Nov2017
        V2  Alexander E. Vaughn 24Nov2017  Took out by-date analyses due to limitations of tweepy
        V3  Alexander E. Vaughn 27Nov2017  Added upper casing for fn and hashtags and fixed polxhashtag
                                           graphs
        V4  Alexander E. Vaughn 27Nov2017  Added hashtag percentage graphs and removed 'na' from
                                           sentiment frequency graphs
Assumptions:

Inputs:
    Data:
        <piped data>.txt           ->  JSON table of tweets from listening period

    Modules:

        Pandas                     ->  data analysis package
        Matplotlib                 ->  data plotting package
        JSON                       ->  data storage package
        Numpy                      ->  data summarization methods package
        Pylab                      ->  graph formatting package

Outputs:
    <Console Output>

Table of Contents:

    #Step 1: Import data from JSON table

    #Step 2: Variable Manipulation

    #Step 3: Sentiment Analysis

"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

#Step 1: Import data from JSON table

data_pull = 'Yes'

if data_pull == 'Yes':
    tweets_data_path = r'<USER INPUT>'
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    #Store in dataframe

tweets = pd.DataFrame()

    #Extract key variables

tweets['text'] = list(map(lambda tweet: tweet.get('text', None), tweets_data))

tweets['lang'] = list(map(lambda tweet: tweet.get('lang', None), tweets_data))

tweets['country'] = map(lambda tweet: tweet.get('place', {}).get('country', {}).get('country') , tweets_data)

tweets['name'] = list(map(lambda tweet: tweet.get('name', None), tweets_data))

tweets['coordinates'] = list(map(lambda tweet: tweet.get('coordinates', None), tweets_data))

tweets['datetime'] = list(map(lambda tweet: tweet.get('created_at', None), tweets_data))

#Step 2: Variable Manipulation

    #parse (RT)

tweets['RT_Ind'] = np.where(tweets['text'].str[:2]=='RT', 'True', 'False')

tweets['Actual_Text'] = np.where(tweets['RT_Ind']=='True', tweets['text'].str.split(':').str[1], tweets['text'])

tweets.loc[tweets['Actual_Text'].str.contains('<USER INPUT>', case = False, na = False), 'Pre_choice1_Ind'] = 'True'
tweets['choice1_Ind'] = np.where(tweets['Pre_choice1_Ind'] == 'True','True','False')
tweets.loc[tweets['Actual_Text'].str.contains('<USER INPUT>', case = False, na = False), 'Pre_choice2_Ind'] = 'True'
tweets['choice2_Ind'] = np.where(tweets['Pre_choice2_Ind'] == 'True','True','False')
conditions = [
    (tweets['choice1_Ind'] == 'True') & (tweets['choice2_Ind'] != 'True'),
    (tweets['choice1_Ind'] != 'True') & (tweets['choice2_Ind'] == 'True')]
choices = ['<USER INPUT>', '<USER INPUT>']
tweets['Candidate_Ind'] = np.select(conditions, choices, default='na')

tweets['created_at'] = pd.to_datetime(tweets['datetime'])
tweets['Date'] = tweets['created_at'].dt.date
tweets['hashtag'] = tweets.Actual_Text.str.extract(r'#(.*?) ')
tweets['hashtag'] = tweets['hashtag'].str.upper()

#Step 3: Sentiment Analysis

    #Run Sentiment Analysis

from textblob import TextBlob

tweets['Polarity'] = tweets.apply(lambda x: TextBlob(str(x['Actual_Text'])).sentiment.polarity, axis=1)
tweets['Subjectivity'] = tweets.apply(lambda x: TextBlob(str(x['Actual_Text'])).sentiment.subjectivity, axis=1)

    #Eliminate zero results

tweets_v2 = pd.DataFrame(tweets.loc[tweets['Polarity'] != 0])

    #Create Polarity Indicator, boolean indicator for 'polarity'

tweets_v2['Pol_Ind'] = np.where(tweets_v2['Polarity'] < 0,'Negative','Positive')

#Step 4: Analyses

    #Histograms by Candidate

histchoice1 = pd.DataFrame(tweets_v2.loc[tweets_v2['Candidate_Ind'] == '<USER INPUT>'])
histchoice1.hist(column='Polarity', bins=50)
pl.title("<USER INPUT> Sentiment")

histchoice2 = pd.DataFrame(tweets_v2.loc[tweets_v2['Candidate_Ind'] == '<USER INPUT>'])
histchoice2.hist(column='Polarity', bins=50)
pl.title("<USER INPUT> Sentiment")

    #show all current graphs
plt.show()
