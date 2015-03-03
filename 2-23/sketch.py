#!/usr/bin/env python
import json
import oauth2 as oauth
import urllib
import urlparse
import unirest
import random
import twitter

creds = json.load(open('/root/Thesis/meditation/configuration.json'))
access_token_url = 'https://www.instapaper.com/api/1/oauth/access_token'

consumer = oauth.Consumer(creds['instapaper_consumer_key'], creds['instapaper_consumer_secret'])
client = oauth.Client(consumer)
client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())

params = {}
params["x_auth_username"] = creds['instapaper_username']
params["x_auth_password"] = creds['instapaper_password']
params["x_auth_mode"] = 'client_auth'

response, token = client.request(access_token_url, method='POST', body=urllib.urlencode(params))

request_token = dict(urlparse.parse_qsl(token))

token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
http = oauth.Client(consumer, token)

response, data = http.request('https://www.instapaper.com/api/1/bookmarks/list', method='POST', body=urllib.urlencode({
    'limit': '50'
})) 

bookmarks = json.loads(data)

def get_concepts(url):
	encoded_url = urllib.quote(url, '')

	response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedConcepts",
		headers={
			"Accept": "text/plain"
		},
		params={
			'url': encoded_url,
			'apikey': creds['alchemy_key'],
			'maxRetrieve': 20,
			'outputMode': 'json'
		}
	)

	cs = []

	for c in response.body['concepts']:
		cs.append(c['text'])
		# print c['text']

	return cs

def concept_net(tag):
	encoded_tag = urllib.quote(tag.lower(), '')
	uri = 'http://conceptnet5.media.mit.edu/data/5.3/c/en/' + encoded_tag

	limit = 10

	response = unirest.get(uri, 
			headers= {
				"Accept": "text/plain"
			},
			params={
				'limit': limit
			})

	edges = response.body['edges']

	surfaceTexts = []
	cleanedTexts = []

	if edges:
		for e in edges:
			if e['surfaceText']:
				surfaceTexts.append(e['surfaceText'])
		for text in surfaceTexts:
			a = text.replace('[','')
			b = a.replace(']','')
			cleanedTexts.append(b)
			# print b
	# else:
	# 	print response.body

	return cleanedTexts

all_concepts = []
all_phrases = []

index = random.randint(2,len(bookmarks) - 1)


bookmark = bookmarks[index]['url']

# print bookmark

all_concepts = get_concepts(bookmark)

for c in all_concepts:
	temp_phrases = concept_net(c)
	if temp_phrases:
		for t in temp_phrases:
			all_phrases.append(t)

# print all_phrases

index = random.randint(0,len(all_phrases) - 1)

phrase = all_phrases[index]

# print phrase

##################
##				##
##	TWITTER 	##
##				##
##################

CONSUMER_KEY = creds["jffng_bot_twit_key"]
CONSUMER_SECRET = creds["jffng_bot_twit_secret"]

OAUTH_TOKEN = creds["jffng_bot_twit_token"]
OAUTH_TOKEN_SECRET = creds["jffng_bot_twit_token_secret"]

twitter_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twit_user = twitter.Twitter(auth=twitter_auth)

tweet = phrase + ' -- ' + bookmark

print tweet

twit_user.statuses.update(status=tweet)
