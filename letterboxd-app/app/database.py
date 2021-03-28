import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
from app import app

def connect_db():
	conn = psycopg2.connect(database='letterboxddb')
	return conn

def get_db():
	if 'db_conn' not in g:
		g.db_conn = connect_db()
	
	return g.db_conn

@app.teardown_appcontext
def teardown_db(error):
	if 'db_conn' in g:
		print('****CLOSING CONNECTION TO DB****')
		g.db_conn.close()
		g.pop('db_conn', None)

def select(query):
	cur = get_db().cursor(cursor_factory=RealDictCursor)
	cur.execute(query)
	res = cur.fetchall()
	cur.close()
	return res