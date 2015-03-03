import json, urllib, urlparse, unirest
from datetime import datetime, timedelta
from sentsql.database import Base, db_session, engine
from sentsql.model import Concept, Bookmark
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask import Flask, Response, request, send_file, send_from_directory

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/node_modules/<path:path>")
def send_module(path):
	return send_from_directory('node_modules', path)

@app.route("/load")
def load():
	title = ['x']
	timeseries = []
	sentiment = ['sentiment']

	all_bookmarks = []
	last_seven_days = []

	for i in db_session.query(Bookmark).all():
		unixtime = int(i.date_read)
		data = {
			'time': datetime.fromtimestamp(unixtime),
			'title': i.title,
			'sentiment': i.sentiment_score
		}

		all_bookmarks.append(data)

	for b in all_bookmarks:
		if b['time'] > (datetime.now() - timedelta(days=7)):
			last_seven_days.append(b)

	last_seven_days = sorted(last_seven_days, key=lambda b: b['time'])

	for l in last_seven_days:
		timeseries.append(l['time'].strftime('%Y-%m-%d'))
		title.append(l['title'])
		sentiment.append(float(l['sentiment'])*100)

	data = {
		'time': timeseries,
		'title': title,
		'sentiment': sentiment
	}

	return json.dumps(data)

if __name__ == '__main__':
	app.run(debug=True)