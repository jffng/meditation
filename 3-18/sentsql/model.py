from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sentsql.database import Base

bookmark_concept = Table('bookmark_concept', Base.metadata,
	Column('bookmark_id', Integer, ForeignKey('bookmark.id'), nullable=False),
	Column('concept_id', Integer, ForeignKey('concept.id'), nullable=False))

class Bookmark(Base):
	__tablename__ = 'bookmark'
	id = Column(Integer, primary_key=True)
	ip_bookmark_id = Column(Integer, nullable=False)
	date_read = Column(Integer, nullable=False)
   	title = Column(String(200), nullable=False)
	url = Column(String(200), nullable=False)
	concepts = relationship('Concept', backref='bookmarks', secondary='bookmark_concept')
	sentiment_score = Column(Float, nullable=False)
	sentiment_type = Column(String(30), nullable=True)
	mixed = Column(Boolean, nullable=True)
	data = Column(Text, nullable=False)

	def __repr__(self):
		return '<Bookmark {}>'.format(self.ip_bookmark_id)

class Concept(Base):
	__tablename__ = 'concept'
	id = Column(Integer, primary_key=True)
	tag = Column(String(140), nullable=False)

	def __repr(self):
		return '<Concepts {}>'.format(self.tag)
