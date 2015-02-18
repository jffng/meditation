import flickrapi
import json

creds = json.load(open('../configuration.json'))

api_key = creds['flickr_key']
api_secret = creds['flickr_secret']

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')

photos = flickr.photos.search(tags='beaches', per_page='10')

parsed = json.loads(photos.decode('utf-8'))

print json.dumps(parsed)