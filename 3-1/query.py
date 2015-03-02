import json, urllib, urlparse, unirest, datetime
from sentsql.database import Base, db_session, engine
from sentsql.model import Concept, Bookmark
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask import Flask, Response, request, send_file

for i in db_session.query(Bookmark).all():
	print i

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/load")
def index():

	for i in db_session.query(Bookmark).all():
		timeseries.append(i.date_read)
		sentiment.append(i.sentiment_score)
	
	timeseries = []
	sentiment = []

	data = {
		'time': timeseries,
		'sentiment': sentiment
	}

	return data

if __name__ == '__main__':
	app.run(debug=True)