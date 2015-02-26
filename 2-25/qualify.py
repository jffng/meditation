from pattern.en import parsetree
from pattern.search import search
import twitter, json, random

creds = json.load(open('/root/Thesis/meditation/configuration.json'))

CONSUMER_KEY = creds["jffng_twit_key"]
CONSUMER_SECRET = creds["jffng_twit_secret"]
OAUTH_TOKEN = creds["jffng_twit_token"]
OAUTH_TOKEN_SECRET = creds["jffng_twit_token_secret"]
BOT_CONSUMER_KEY = creds["qualify_twit_key"]
BOT_CONSUMER_SECRET = creds["qualify_twit_secret"]
BOT_OAUTH_TOKEN = creds["qualify_twit_token"]
BOT_OAUTH_TOKEN_SECRET = creds["qualify_twit_token_secret"]

jffng_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_userstream = twitter.TwitterStream(auth=jffng_auth, domain='userstream.twitter.com')

statuses = twitter_userstream.user()

qualify_auth = twitter.oauth.OAuth(BOT_OAUTH_TOKEN, BOT_OAUTH_TOKEN_SECRET, BOT_CONSUMER_KEY, BOT_CONSUMER_SECRET)

qualify_user = twitter.Twitter(auth=qualify_auth)

qualifiers = ['maybe', 'perhaps', 'supposedly', 'possibly', 'likely', 'conceivably', 'potentially']

for t in statuses:
	try:
		tw = t['text']
		# print tweet
		s = parsetree(tw, relations=True, lemmata=True)
		matches = search('NP will|be RB?+ PP|VP|ADJP|ADVP|NP', s)
		if matches:
			qualifier = qualifiers[random.randint(0,len(qualifiers)-1)]

			fragments = tw.split(matches[0].string)
			
			if fragments[1]:
				status = fragments[0] + matches[0].string + ', ' + qualifier + ',' + fragments[1]
			else:
				status = fragments[0] + matches[0].string + ', ' + qualifier + '.'			
			
			status = status.replace('@', '')

			if len(status) > 139:
				# print len(status)
				status = status[:139]
			# print status
			qualify_user.statuses.update(status=status)
	
	except (KeyError, IndexError):
		pass
