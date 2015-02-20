import json
import unirest
import urllib2

creds = json.load(open('../configuration.json'))

def get_ig_id(query):
	ig_response = unirest.get("https://api.instagram.com/v1/users/search", 
		headers= {
			"Accept": "text/plain"
		},
		params={
			'q': query,
			'access_token': creds['ig_token']
		})

	return ig_response.body['data'][0]['id']

def get_ig_media(uid):
	ig_get = 'https://api.instagram.com/v1/users/self/feed' 

	user_response = unirest.get(ig_get, 
		headers={
			"Accept": "text/plain"
		},
		params={
			'access_token': creds['ig_token'],
			'count': 20
		})

	return user_response.body['data']

q = 'jffng'

id = get_ig_id(q)

media = get_ig_media(id)

#for i in media:
#	print i['images']['standard_resolution']['url']
imagedir = '~/Thesis/meditation/2-19/ig/'

for m in media:
	f = urllib2.urlopen(m['images']['standard_resolution']['url'])
	data = f.read()
	with open('ig/' + m['id'] + '.jpg', "wb") as code:
		code.write(data)
