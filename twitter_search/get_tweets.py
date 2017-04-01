import tweepy
from tweepy import OAuthHandler
import csv

### AUTHENTICATE ############################################################

# Authenticating with Twitter App
consumer_key = 'V4DwZPB6fGwsgUN5h27Cmv1zi'
consumer_secret = 'DJh4h0FaEgCeGZ5GwCWE5Pxvp1vHtpWfNkIGtk896dzGgIf51K'
access_token = '741486000-T0sijZatp5ZmxbA0MgHwgtqGKjh4WNKHhP3IqquJ'
access_secret = 'D89rXSqveZLLnfVWnf8jS1SX2jn7TlYnZ7TAvT9JBTajh'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

### RETRIEVES TWEETS FROM CARDIFF AREA ###########################

tweet_id = 0
tweet = ''
tweet_ids = []
tweet_dict = {}

# Specifies tweets being queried by search criteria ("q") and geocode
cardiff_tweets = tweepy.Cursor(api.search, q = '', geocode = "51.49675,-3.19229,16km").items(30)

# Loop through returned tweets
for tweet in cardiff_tweets:
	tweet_id += 1
	tweet_ids.append (tweet_id)
	tweet_string = str(tweet.text)
	tweet_dict[tweet_id] = tweet_string

print(tweet_dict)

