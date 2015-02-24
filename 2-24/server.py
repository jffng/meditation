from flask import Flask, Response, request, send_file
import unirest
import urllib
import flickrapi
import json
import random
import os
import subprocess
from subprocess import Popen, PIPE
import os

app = Flask(__name__)
app.config.from_object(__name__)
creds = json.load(open('../configuration.json'))

f = open('../ccv/samples/image-net-2012.words')

# strips the extra line break added by iterating over the file
temp = [line[:-1] for line in f]

words_list = []

for line in temp:
	words_list.append(line)

f.close()

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
	encoded = urllib.quote(img_url, '')

	response = unirest.get("http://access.alchemyapi.com/calls/url/URLGetRankedImageKeywords",
		headers={
			"Accept": "text/plain"
		},
		params={
			'url': encoded,
			'forceShowAll': 1,
			'apikey': creds['alchemy_key'],
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
	photo = parsed['photos']['photo'][random.randint(0,len(parsed)-1)]
	# https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

	url = 'https://farm'+str(photo['farm'])+'.staticflickr.com/'+str(photo['server'])+'/'+str(photo['id'])+'_'+str(photo['secret'])+'.jpg'

	print url
	return url

def learn_deep(args):
	p = subprocess.Popen(args, stdout=PIPE, shell=True)

	data, err = p.communicate(input=None)

	tags = data.split('\n')
	tag_set = []

	for t in tags:
		if t:
			tag, confidence = t.split()
			if (float(confidence) > .05):
				tag_set.append(words_list[int(tag)-1].split(', '))

	return tag_set

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/submit", methods=['GET','POST'])
def submit():
	uid = get_ig_id('jffng')

	ig_media = get_ig_media(uid)
	
	image_list = []
	all_tags = []

	index = 19

	for i in os.listdir('ig'):
		if i.endswith(".jpg"): 
			print image_list

			ig_url = ig_media[index]['images']['standard_resolution']['url']
			args = ['./../ccv/bin/cnnclassify ig/%s ../ccv/samples/image-net-2012.sqlite3' % i]
			tags = learn_deep(args)

			ig_flickr = []
			ig_flickr.append(str(ig_url))

			flickr_url = search_flickr(str(tags))			
			ig_flickr.append(str(flickr_url))

			tagset = []
			for t in tags:
				tagset.append(t[0])
			ig_flickr.append(tagset)
			
			image_list.append(ig_flickr)

			index-=1
			continue
		else:
			continue

	print image_list

	return json.dumps(image_list)

	# for i in ig_media:
	# 	print image_list
	# 	ig_flickr = []

	# 	ig_flickr.append(str(ig_url))

	# 	tags = []

	# 	# tags = get_img_tags(str(ig_url))
	# 	if (tags):
	# 		tagset = ''
	# 		for t in tags:
	# 			tagset += str(t['text']) + ','
	# 		flickr_url = search_flickr(tagset)			
	# 		ig_flickr.append(str(flickr_url))
	# 		ig_flickr.append(tagset[:-1])
	# 		image_list.append(ig_flickr)

	# 	else:
	# 		ig_flickr.append(str(ig_url))
	# 		ig_flickr.append('----')
	# 		image_list.append(ig_flickr)

	# print image_list

	# return json.dumps(image_list)

if __name__ == '__main__':
	app.run(debug=True)




