# I have three reference points

# 1. Article read + recommendation
# 2. Check in / location on Foursquare
# 3. Song from Spotify
# 4. Media purchase on amazon
# 5. Last thing you watched on Netflix

# algorithm that mediates, permeates, defines, understands, sees, predicts, recommends.

# What of the stories / IDENTITIES that we construct around the behaviors on media channels? 
# 
# Twitter bio. 
# 
# That moment when

import unirest, json
import oauth2 as oauth
creds = json.load(open('../configuration.json'))

# # Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=creds['jffng_twit_key'], secret=creds['jffng_twit_secret'])

# Request token URL for Twitter.
request_token_url = "https://twitter.com/oauth/request_token"

# Create our client.
client = oauth.Client(consumer)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url, "GET")
# print resp
# print content

params = {
	'screen_name': 'viccoho',
	'count': 20
}

resp, content = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=vicciho&count=1', "GET")

print resp