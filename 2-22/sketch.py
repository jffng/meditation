import json
import subprocess
from subprocess import Popen, PIPE
import os
from nltk.stem.wordnet import WordNetLemmatizer
import unirest

f = open('../ccv/samples/image-net-2012.words')

# strips the extra line break added by iterating over the file
temp = [line[:-1] for line in f]

words_list = []

for line in temp:
	words_list.append(line)

f.close()

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
				lm = lmtzr.lemmatize(t[0])
				all_tags.append(lm)
		print all_tags
		continue
	else:
		continue

for tag in all_tags:
