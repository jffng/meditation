#!/usr/bin/env python
import json
import oauth2 as oauth
import urllib
import urlparse
import unirest

creds = json.load(open('../configuration.json'))
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
    'limit': '20'
})) 

bookmarks = json.loads(data)

# url = bookmarks[2]['url']

def get_concepts(url):
	encoded_url = urllib.quote(url, '')

	response = unirest.get('http://interest-graph.getprismatic.com/url/topic',
		headers={
			"Accept": "text/plain",
			'X-API-TOKEN': creds['prismatic_key']		
		},
		params={
			'url': encoded_url,
		}
	)

	concepts = []

	try:
		for t in response.body['topics']:
			concepts.append(t['topic'])
	except TypeError:
		return

	return concepts

def get_sentiment(phrase):
	sentiment = unirest.get("http://access.alchemyapi.com/calls/text/TextGetTextSentiment",
				headers={
					"Accept": "text/plain"
				},
				params={
					'apikey': creds['alchemy_key_2'],
					'text': phrase,
					'outputMode': 'json'
				}
			)

	try:
		print phrase + ": " + sentiment.body['docSentiment']['score']
		return float(sentiment.body['docSentiment']['score'])
	except KeyError:
		print phrase + ": neutral"
		return 0	

# all_concepts = []
# cs_list = []

# for b in bookmark[2:]:
# 	cs_list = get_concepts(b['url'])
# 	for i in cs_list:
# 		all_concepts.append(i)

# sentiment=0

# for c in all_concepts:
# 	sentiment+=get_sentiment(c)

# sentiment=sentiment/len(all_concepts)

# print "How Jeff feels: " , sentiment

all_concepts = []

for b in bookmarks[2:]:
	concept_list = get_concepts(b['url'])
	if (concept_list != None):
		for c in concept_list:
			all_concepts.append(c)

sentiment = 0

for c in all_concepts:
	sentiment+=get_sentiment(c)

print "How Jeff feels: " , sentiment


