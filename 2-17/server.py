from flask import Flask, Response, request, send_file
import unirest
import urllib
import flickrapi
import json
import random

app = Flask(__name__)
app.config.from_object(__name__)
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
	ig_get = 'https://api.instagram.com/v1/users/' + uid + '/media/recent' 

	user_response = unirest.get(ig_get, 
		headers={
			"Accept": "text/plain"
		},
		params={
			'access_token': creds['ig_token'],
			'count': 20
		})

	return user_response.body['data']
	# [14]['images']['standard_resolution']['url']

def get_img_tags(img_url):
	response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedImageKeywords",
		headers={
			"Accept": "text/plain"
		},
		params={
			'url': img_url,
			'forceShowAll': 1,
			'apikey': creds['alchemy_key_2'],
			'outputMode': 'json'
		}
	)

	return response.body['imageKeywords']

def search_flickr(ig_tags):
	api_key = creds['flickr_key']
	api_secret = creds['flickr_secret']
	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')

	photos = flickr.photos.search(tags=ig_tags, per_page='10')
	parsed = json.loads(photos.decode('utf-8'))
	photo = parsed['photos']['photo'][random.randint(0,9)]
	# https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

	url = 'https://farm'+str(photo['farm'])+'.staticflickr.com/'+str(photo['server'])+'/'+str(photo['id'])+'_'+str(photo['secret'])+'.jpg'

	print url
	return url

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/submit", methods=['GET','POST'])
def submit():
	uid = get_ig_id('jffng')

	ig_media = get_ig_media(uid)
	
	image_list = []

	for i in ig_media:
		print image_list
		ig_flickr = []

		ig_url = i['images']['standard_resolution']['url']
		ig_flickr.append(str(ig_url))

		tags = get_img_tags(str(ig_url))
		if (tags):
			tagset = ''
			for t in tags:
				tagset += str(t['text']) + ','
			flickr_url = search_flickr(tagset)			
			ig_flickr.append(str(flickr_url))
			ig_flickr.append(tagset[:-1])
			image_list.append(ig_flickr)

		else:
			ig_flickr.append(str(ig_url))
			ig_flickr.append('----')
			image_list.append(ig_flickr)

	print image_list

	return json.dumps(image_list)

if __name__ == '__main__':
	app.run(debug=True)




