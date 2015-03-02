import json, urllib, urlparse, unirest, datetime
from sentsql.database import Base, db_session, engine
from sentsql.model import Concept, Bookmark
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

for i in db_session.query(Bookmark).all():
	print i