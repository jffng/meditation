import json, urllib, urlparse, unirest
from datetime import datetime, timedelta
import oauth2 as oauth
from sentsql.database import Base, db_session, engine
from sentsql.model import Concept, Bookmark
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

creds = json.load(open('../configuration.json'))
access_token_url = 'https://www.instapaper.com/api/1/oauth/access_token'

consumer = oauth.Consumer(creds['instapaper_consumer_key'], creds['instapaper_consumer_secret'])
client = oauth.Client(consumer)
client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())

params = {}
params["x_auth_username"] = creds['instapaper_username']
params["x_auth_password"] = creds['instapaper_password']
params["x_auth_mode"] = 'client_auth'

response, token = client.request(access_token_url, method='POST', body=urllib.urlencode(params))

request_token = dict(urlparse.parse_qsl(token))

token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
http = oauth.Client(consumer, token)

response, data = http.request('https://www.instapaper.com/api/1/bookmarks/list', method='POST', body=urllib.urlencode({
    'limit': '50'
})) 

unread = json.loads(data)

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

    concepts = []

    for c in response.body['concepts']:
        concepts.append(c['text'])

    response = unirest.get('http://interest-graph.getprismatic.com/url/topic',
        headers={
            "Accept": "text/plain",
            'X-API-TOKEN': creds['prismatic_key']
        },
        params={
            'url': encoded_url,
        }
    )

    try:
        for t in response.body['topics']:
            concepts.append(t['topic'])
    except TypeError:
        pass
        
    return set(concepts)

def get_sentiment(url):
    sentiment = unirest.get("http://access.alchemyapi.com/calls/url/URLGetTextSentiment",
                headers={
                    "Accept": "text/plain"
                },
                params={
                    'apikey': creds['alchemy_key_2'],
                    'url': url,
                    'showSourceText': 1,
                    'sourceText': 'cleaned_or_raw',
                    'outputMode': 'json'
                }
            )

    try:
        return {
            'type': str(sentiment.body['docSentiment']['type']),
            'score': float(sentiment.body['docSentiment']['score']),
            'text': sentiment.body['text'],
            'mixed': int(sentiment.body['docSentiment']['mixed'])
        }
    except KeyError:
        return 0   

def db_commit(b):
	try:
		b_obj = db_session.query(Bookmark).filter_by(ip_bookmark_id=b['ip_bookmark_id']).one()
	except MultipleResultsFound:
		pass
	except NoResultFound:
		try:
			sentiment = get_sentiment(b['url'])
			concepts = get_concepts(b['url'])

			if int(sentiment['mixed']) == 1:
				mixed = True
			else:
				mixed = False

			b_obj = Bookmark(date_read=b['date'],ip_bookmark_id=b['ip_bookmark_id'],title=b['title'],url=b['url'],
			sentiment_score=sentiment['score'],sentiment_type=sentiment['type'],mixed=mixed, data=json.dumps(sentiment['text']))     

			try:
				for c in concepts:
					try:
						c_obj = db_session.query(Concept).filter(Concept.tag == c).one()
						b_obj.concepts.append(c_obj)
					except MultipleResultsFound:
						pass
					except NoResultFound:
						c_obj = Concept(tag=c)
						db_session.add(c_obj)
						db_session.commit()
						b_obj.concepts.append(c_obj)
					except OperationalError:
						db_session.rollback()
				db_session.add(b_obj)
				db_session.commit()
			except OperationalError:
				db_session.rollback()
		except TypeError:
			db_session.rollback()


for b in unread[2:]:
	bookmark = {
		'date': b['time'],
		'title': b['title'],
		'url': b['url'],
		'ip_bookmark_id': b['bookmark_id'],
	}

	db_commit(bookmark)

