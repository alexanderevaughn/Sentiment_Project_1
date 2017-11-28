# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:16:16 2017

Purpose: To create the data for a sentiment analysis for a binary choice.

@author: Alexander E. Vaughn

Updates:
        V1  Alexander E. Vaughn  01Nov2017

Assumptions:

Notes:
    Form of Call:                  ->  <in prompt>python Level_1.py > twitter_data.txt
    Source for early portion       ->  http://adilmoujahid.com/posts/2014/07/twitter-analytics/

Inputs:

    Data:
        twitter API        ->  input data from twitter

    Modules:
        Pandas             ->  data analysis package
        Tweepy             ->  Twitter API connection package

Outputs:

    <piped data>.txt       ->  JSON table of tweets from listening period

Table of Contents:

    #Step 1: Import data

"""
    #Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd

#Step 1: Import data

    #Variables that contains the user credentials to access Twitter API
access_token = "<USER INPUT>"
access_token_secret = "<USER INPUT>"
consumer_key = "<USER INPUT>"
consumer_secret = "<USER INPUT>"


    #This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

        #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=[<USER INPUT>])
