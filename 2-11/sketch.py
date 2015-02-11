import unirest

ig_response = unirest.get("https://api.instagram.com/v1/users/search", 
	headers= {
		"Accept": "text/plain"
	},
	params={
		'q': 'jffng',
		'access_token': 'your_token'
	})

user_id = ig_response.body['data'][0]['id']

ig_get = 'https://api.instagram.com/v1/users/' + str(user_id) + '/media/recent' 

user_response = unirest.get(ig_get, 
	headers={
		"Accept": "text/plain"
	},
	params={
		'access_token': 'your_token'
	})

img_url = user_response.body['data'][14]['images']['standard_resolution']['url']
print img_url

response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedImageKeywords",
	headers={
		"Accept": "text/plain"
	},
	params={
		'url': img_url,
		'forceShowAll': 1,
		'apikey': 'your_key',
		'outputMode': 'json'
	}
)

print response.body['imageKeywords']

image_sentiment = {}

for i in response.body['imageKeywords']:
	sentiment = unirest.get("http://access.alchemyapi.com/calls/text/TextGetTextSentiment",
		headers={
			"Accept": "text/plain"
		},
		params={
			'apikey': 'your_key',
			'text': i['text'],
			'outputMode': 'json'
		}
	)

	try:
		print i['text'] + ': ' + sentiment.body['docSentiment']['score']
		image_sentiment[i['text']] = sentiment.body['docSentiment']['score']
	except KeyError:
		print i['text'] + ': Neutral'	
	

# print image_sentiment