from flask import Flask, Response, request, send_file
import unirest
import urllib
import json

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
	return send_file('templates/index.html')

@app.route("/sentiments", methods=['GET','POST'])
def submit():
	url = request.args['url']

	def get_concepts_sentiment(url):
		url_encoded = urllib.quote(url, '')
		response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedConcepts",
			headers={
				"Accept": "text/plain"
			},
			params={
				'url': url_encoded,
				'apikey': '',
				'maxRetrieve': 20,
				'outputMode': 'json'
			}
		)

		concept_sentiment = {}

		for c in response.body['concepts']:
			sentiment = unirest.get("http://access.alchemyapi.com/calls/text/TextGetTextSentiment",
				headers={
					"Accept": "text/plain"
				},
				params={
					'apikey': '',
					'text': c['text'],
					'outputMode': 'json'
				}
			)

			try:
				print c['text'] + ': ' + sentiment.body['docSentiment']['score']
				concept_sentiment[c['text']] = sentiment.body['docSentiment']['score']
			except KeyError:
				print c['text'] + ': Neutral'	

		return concept_sentiment

	return Response(json.dumps(get_concepts_sentiment(url)))

if __name__ == '__main__':
	app.run(debug=True)

