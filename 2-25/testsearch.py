from pattern.en import parsetree
from pattern.search import search

tweet = 'RT @nytimesarts: Lady Gaga is starring in American Horror Story http://t.co/NiryZGzzPW aj;dadkklsdfka;lsdfjk;asdfjk;sdjf;jakl;sfjkaks;df;akfds;jkadf;ljjlajksdfasdbfkjasjdklfbaljskdbfjkabdfjkdaadlksfj;'

s = parsetree(tweet, encoding='utf-8', relations=True, lemmata=True)
matches = search('NP will|be RB?+ PP|VP|ADJP|ADVP|NP', s)
if matches:
	status = tweet.split(matches[0].string)[0] + matches[0].string + ', maybe,' + tweet.split(matches[0].string)[1]
	status = status.replace('@', '')
	if len(status) > 139:
		print len(status)
		status = status[:139]
	print status
	# print match.constituents()[-1], '=>', match.constituents()[0]