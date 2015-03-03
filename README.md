# meditation

daily practice working towards ITP Thesis 2015. goal: one function, object, pseudocode -- conceptual "sketch" -- a day.

##### 2-6
Uses speech recognition and determines the sentiment of what was said. Changes color of the page based on the statement's positivity or negativity. Adapted from a Lauren McCarthy example from Conversation + Computation class at ITP Spring 2015. 

##### 2-8
Feed an article to AlchemyAPI, tags the concepts in the articles, returns the positivity / negativity scores associated with the non-neutral concepts. Tells you whether or not the article will make you happy. 

##### 2-11
Takes a user's instagram image, tags it via Alchemy, rates the sentiment of each tag.

##### 2-16
Feeds articles I've read via Instapaper to Alchemy API; Alchemy tags the concepts + rates their sentiment; the sketch returns an average of my positivity / negativity

##### 2-17
Feeds my Instagram images into image tagger, searches Flickr api for images with those tags, and replaces on mouse rollover.

##### 2-18
Same as 2-16, but uses Prismatic's Interest Graph API.

##### 2-19
An attempt to grab my Instagram images and tag using a pre-trained Deep Learning network. 

##### 2-20
Beginning of a generative, daily audio-biography / snapshot / "portrait"

##### 2-22
Uses a convolutional neural network (libccv) to tag instagram images and generate related concepts

##### 2-23
Tags concepts in a random article I've read, finds the text relationship, tweets it out.

##### 2-24
Adapts 2-17 example to use libccv instead of Alchemy's image tagger

##### 2-25
Searches my twitter timeline for declarative / fact-oriented tweets, adds qualification (e.g. "maybe", "perhaps")

##### 2-27
Idea for generating audio stories 

##### 3-1
Database of article - concept - sentiment. Plots sentiment of articles read over the last 7 days, makes a recommendation.

##### 3-2
Checks for new articles, logs them to the db.