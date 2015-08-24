#!/usr/bin/env python
import json
import oauth2 as oauth
import urllib
import urlparse
import unirest
import random
import twitter
import wordfilter as wf

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
    'limit': '100'
})) 

bookmarks = json.loads(data)
bookmarks = bookmarks[2:]

response, data = http.request('https://www.instapaper.com/api/1/bookmarks/list', method='POST', body=urllib.urlencode({
    'limit': '100',
    'folder_id': 'archive'
})) 

archive = json.loads(data)
archive = archive[2:]

for a in archive:
	bookmarks.append(a)

def get_concepts(url):
	encoded_url = urllib.quote(url, '')

	response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedConcepts",
		headers={
			"Accept": "text/plain"
		},
		params={
			'url': encoded_url,
			'apikey': creds['alchemy_key_2'],
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
	uri = 'http://conceptnet5.media.mit.edu/data/5.4/c/en/' + encoded_tag

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
                                temp = {}
                                temp['start'] = e['surfaceStart'].replace(' ', '')
                                temp['end'] = e['surfaceEnd'].replace(' ', '')
                                temp['text'] = e['surfaceText']
                                surfaceTexts.append(temp)
				#surfaceTexts.append(e['surfaceText'])
		for t in surfaceTexts:
			a = t['text'].replace('[','')
			b = a.replace(']','')
			t['text'] = b
			ht = '#' + t['start']
                        t['text'] = ht.join(t['text'].rsplit(t['start'], 1))
                        ht = '#' + t['end']
                        t['text'] = ht.join(t['text'].rsplit(t['end'], 1))
	                cleanedTexts.append(t['text'])
                        #print t['text']
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
                        if t.find('#') != -1:
			        all_phrases.append(t)

# print all_phrases

index = random.randint(0,len(all_phrases) - 1)

phrase = all_phrases[index]
#print phrase

filter = wf.Wordfilter()

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

if filter.blacklisted(phrase):
	pass
else:
        print tweet
        twit_user.statuses.update(status=tweet)
