import unirest, json, urllib

creds = json.load(open('../configuration.json'))

def get_concepts(url):
	encoded_url = urllib.quote(url, '')

	response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedConcepts",
		headers={
			"Accept": "text/plain"
		},
		params={
			'url': encoded_url,
			'apikey': creds['alchemy_key_3'],
			'maxRetrieve': 20,
			'outputMode': 'json'
		}
	)

	# print response.body

	concepts = []

	for c in response.body['concepts']:
		concepts.append(c['text'])

	return concepts

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

	print response.body

	try:
		for t in response.body['topics']:
			concepts.append(t['topic'])
	except TypeError:
		pass

	return set(concepts)

# print get_concepts('http://www.nytimes.com/2015/03/21/us/netanyahu-tactics-anger-many-us-jews-deepening-a-divide.html')

print get_concepts('http://www.jffng.com/writings/21515.html')
