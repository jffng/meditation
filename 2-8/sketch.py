import unirest

# These code snippets use an open-source library. http://unirest.io/python
response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedConcepts",
	headers={
		"Accept": "text/plain"
	},
	params={
		'url': 'http%3A%2F%2Fthenewinquiry.com%2Fessays%2Fthe-anxieties-of-big-data%2F',
		'apikey': 'e553639093ab39a2908def2de1cfc565d6583ae8',
		'maxRetrieve': 20,
		# 'showSourceText': 1,
		'outputMode': 'json'
	}
)

# print response.body['text']

concept_sentiment = {}

for c in response.body['concepts']:
	sentiment = unirest.get("http://access.alchemyapi.com/calls/text/TextGetTextSentiment",
		headers={
			"Accept": "text/plain"
		},
		params={
			'apikey': 'e553639093ab39a2908def2de1cfc565d6583ae8',
			'text': c['text'],
			'outputMode': 'json'
		}
	)

	try:
		print c['text'] + ': ' + sentiment.body['docSentiment']['score']
		concept_sentiment[c['text']] = sentiment.body['docSentiment']['score']
	except KeyError:
		print c['text'] + ': Neutral'	
	

print concept_sentiment