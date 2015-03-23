#!/usr/bin/env python
import json, urllib, urlparse, unirest
from datetime import datetime, timedelta
from sentsql.database import Base, db_session, engine
from sentsql.model import Concept, Bookmark
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import networkx as nx
import re

def graph_add_node(n, g, t):
    if g.has_node(n):
        g.node[n]['weight']+=1
    else:
        g.add_node(n)
        g.node[n]['label'] = n
        g.node[n]['weight'] = 1
        g.node[n]['type'] = t
 
def graph_add_edge(n1, n2, g):
    if g.has_edge(n1, n2):
        g[n1][n2]['weight']+=1
    else:
        g.add_edge(n1,n2)
        g[n1][n2]['weight']=1

graph = nx.Graph()

all_concepts = []

for b in db_session.query(Bookmark).all():
	graph_add_node(b.ip_bookmark_id, graph, 'bookmark')
	for c in b.concepts:
		graph_add_node(c.tag, graph, 'concept')
		graph_add_edge(b.ip_bookmark_id, c.tag, graph)

q = 'concept_map'

# # because it ends up in the file name for the GEXF output file
nx.write_gexf(graph, '{}.gexf'.format(q))
print('{}.gexf'.format(q))

# print len(set(all_concepts))