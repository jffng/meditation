from pattern.en import parsetree
from pattern.search import search
import twitter, json, random

creds = json.load(open('../configuration.json'))

CONSUMER_KEY = creds["jffng_twit_key"]
CONSUMER_SECRET = creds["jffng_twit_secret"]

OAUTH_TOKEN = creds["jffng_twit_token"]
OAUTH_TOKEN_SECRET = creds["jffng_twit_token_secret"]

jffng_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
 
# jffng_user = twitter.Twitter(auth=jffng_auth)

# bot_user = twitter.TwitterStream(auth=bot_auth)

# twitter_stream = twitter.TwitterStream(auth=jffng_auth)

twitter_userstream = twitter.TwitterStream(auth=jffng_auth, domain='userstream.twitter.com')

statuses = twitter_userstream.user()

qualifiers = ['maybe', 'perhaps', 'supposedly', 'possibly', 'likely', 'conceivably', 'potentially']

for t in statuses:
	try:
		tweet = t['text']
		# print tweet
		s = parsetree(t['text'], relations=True, lemmata=True)
		matches = search('NP will|be RB?+ PP|VP|ADJP|ADVP|NP', s)
		if matches:
			qualifier = qualifiers[random.randint(0,len(qualifiers)-1)]
			status = tweet.split(matches[0].string)[0] + matches[0].string + ', ' + qualifier + ',' + tweet.split(matches[0].string)[1]
			status = status.replace('@', '')
			if len(status) > 139:
				print len(status)
				status = status[:139]
			print status
	except KeyError:
		continue
	except IndexError:
		continue