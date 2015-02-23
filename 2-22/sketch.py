import json
import subprocess
from subprocess import Popen, PIPE
import os
from nltk.stem.wordnet import WordNetLemmatizer
import unirest
import random

f = open('../ccv/samples/image-net-2012.words')

# strips the extra line break added by iterating over the file
temp = [line[:-1] for line in f]

words_list = []

for line in temp:
	words_list.append(line)

f.close()

def concept_tag(tag):
	uri = 'http://conceptnet5.media.mit.edu/data/5.3/c/en/' + tag

	limit = 10

	response = unirest.get(uri, 
			headers= {
				"Accept": "text/plain"
			},
			params={
				'limit': limit
			})

	edges = response.body['edges']

	if edges:
		print edges[random.randint(0,len(edges)-1)]['surfaceText']

def learn_deep(args):
	p = subprocess.Popen(args, stdout=PIPE, shell=True)

	data, err = p.communicate(input=None)

	tags = data.split('\n')
	tag_set = []

	for t in tags:
		if t:
			tag, confidence = t.split()
			if (float(confidence) > .1):
				tag_set.append(words_list[int(tag)-1].split(', '))

	return tag_set

all_tags = []

lmtzr = WordNetLemmatizer()

for i in os.listdir('ig'):
	if i.endswith(".jpg"): 
		args = ['./../ccv/bin/cnnclassify ig/%s ../ccv/samples/image-net-2012.sqlite3' % i]
		tags = learn_deep(args)

		for t in tags:
			if len(t) > 0:
				lm = lmtzr.lemmatize(t[0],'v')
				all_tags.append(str(lm))
		# print all_tags
		continue
	else:
		continue

for tag in all_tags:
	concept_tag(tag)

