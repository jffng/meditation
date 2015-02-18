from flask import Flask, Response, request, send_file
import unirest
import urllib
import flickrapi
import json

app = Flask(__name__)
app.config.from_object(__name__)
creds = json.load(open('../configuration.json'))

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/submit", methods=['GET','POST'])
def submit():
	api_key = creds['flickr_key']
	api_secret = creds['flickr_secret']
	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')

	photos = flickr.photos.search(tags='beaches', per_page='10')
	parsed = json.loads(photos.decode('utf-8'))

	return json.dumps(parsed)

if __name__ == '__main__':
	app.run(debug=True)




