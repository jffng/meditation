import unirest

# These code snippets use an open-source library. http://unirest.io/python
response = unirest.get("https://alchemy.p.mashape.com/url/URLGetRankedConcepts?baseUrl=<required>&linkedData=false&outputMode=json&url=http%3A%2F%2Fwww.cnn.com%2F2011%2F09%2F28%2Fus%2Fmassachusetts-pentagon-plot-arrest%2Findex.html%3Fhpt%3Dhp_t1",
	headers={
		"X-Mashape-Key": "z89uguZztpmshQ2wwkurM9CDca1tp1qVMT4jsn4uyYJZkVcTNZ",
		"Accept": "text/plain"
	}
)

for c in response.body['concepts']:
	print c['text']

