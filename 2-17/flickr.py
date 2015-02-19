import flickrapi
import json

creds = json.load(open('../configuration.json'))


def search_flickr(ig_tags):
	api_key = creds['flickr_key']
	api_secret = creds['flickr_secret']
	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')

	photos = flickr.photos.search(tags=ig_tags, per_page='10')
	parsed = json.loads(photos.decode('utf-8'))
	photo = parsed['photos']['photo'][0]
	# https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

	url = 'https://farm'+str(photo['farm'])+'.staticflickr.com/'+str(photo['server'])+'/'+str(photo['id'])+'_'+str(photo['secret'])+'.jpg'

	print url