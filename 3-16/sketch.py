def get_prismatic(url):
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
			print t['topic']
			concepts.append(t['topic'])
	except TypeError:
		return

	return concepts	

creds = json.load(open('../configuration.json'))

# # Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=creds['jffng_twit_key'], secret=creds['jffng_twit_secret'])

# Request token URL for Twitter.
request_token_url = "https://twitter.com/oauth/request_token"

# Create our client.
client = oauth.Client(consumer)
resp, content = client.request(request_token_url, "GET")

resp, content = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=tigoe&count=200', "GET")

data = json.loads(content)

all_concepts = []
individual_concepts = []

for t in data:
	for u in t['entities']['urls']:
		# if 'instagram' in u['expanded_url']:
		# 	pass
		# else:
		p = get_prismatic(u['expanded_url'])
		all_concepts.append(p)

for i in all_concepts:
	if i:
		for c in i:
			individual_concepts.append(c)

print len(individual_concepts)