from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import tweepy

from tweepy.api import API


#twitter API keys
access_token = "778932228244078593-w7FiOTCQ6F2ewyIYam9goHU4GGcCwra"
access_token_secret = "HgovHNpV6NynTTptx3ryIOruRfTddPJhZ3lyx30pnQQz8"
consumer_key = "AXb13KTrpir1lybVEYy84b6sR"
consumer_secret = "bWXmLH89rgDUfuacjfFE9HSVpI2SuAaiaShH8JhzwMWlKyHXbb"

class TweetListener():

    stream = None
    l = None
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    def TweetCollectorThreadFunc(self,searcharray, listener):
        self.l = listener
        self.searchAray = searcharray

        #turns out there is an async function for this so you don't have to thread it.
        #found that out too late.
        self.stream = Stream(self.auth, self.l)
        self.stream.filter(track=[searcharray], async=False)





