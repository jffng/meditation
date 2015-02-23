import unirest
import json
import sys

concept = sys.argv[1]

uri = 'http://conceptnet5.media.mit.edu/data/5.3/c/en/' + concept

limit = 10

response = unirest.get(uri, 
		headers= {
			"Accept": "text/plain"
		},
		params={
			'limit': limit
		})

# parsed = json.loads(response.body)

for e in response.body['edges']:
	if e['surfaceText']:
		print e['surfaceText']
		continue
	else:
		continue