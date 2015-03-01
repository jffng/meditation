#!/usr/bin/env python
import json
import oauth2 as oauth
import urllib
import urlparse
import unirest
import datetime

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

# response, data = http.request('https://www.instapaper.com/api/1/bookmarks/list', method='POST', body=urllib.urlencode({
#     'limit': '100'
# })) 

# bookmarks = json.loads(data)

response, data = http.request('https://www.instapaper.com/api/1/bookmarks/list', method='POST', body=urllib.urlencode({
    'limit': '100',
    'folder_id': 'archive'
})) 

archived = json.loads(data)

for a in archived[2:]:
	thing = datetime.datetime.fromtimestamp(int(a['time'])).strftime('%Y-%m-%d %H:%M:%S')
	print thing

# print bookmarks

# print len(bookmarks[2:])