import tweepy
from config import Twitter

consumer_key        = Twitter.CONSUMER_KEY
consumer_key_secret = Twitter.CONSUMER_KEY_SECRET
access_token        = Twitter.ACCESS_TOKEN
access_token_secret = Twitter.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# This app creates a tweet in DataCloudMag twitter account.

text = "Solving the Gilded Rose Refactoring Kata by @avikoleum."
url = "https://datacloudmag.com/solving-the-gilded-rose-refactoring-kata/"
hashtags = "#python #refactoring"


tweet = f"{text} \n\n{hashtags} \n\n{url}"

# Create the tweet
response = api.update_status(tweet)

print(
    f"""Response ID: {response.id}
    Response Text: {response.text} 
    Created At{str(response.created_at)}"""
)