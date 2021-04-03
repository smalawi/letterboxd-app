import os
import psycopg2

def create_tables():
	"""
	Creates tables in database letterboxddb

	Args: None
	Returns: None
	"""
	conn =  psycopg2.connect("dbname=letterboxddb")
	cursor = conn.cursor()

	cursor.execute("""
		DROP TABLE IF EXISTS movie CASCADE;
		CREATE TABLE movie (
			movie_id	integer PRIMARY KEY,
			movie_name	varchar,
			year		integer,
			movie_href	varchar UNIQUE
		);
	""")

	cursor.execute("""
		DROP TABLE IF EXISTS person CASCADE;
		CREATE TABLE person (
			person_id	varchar PRIMARY KEY,
			person_name	varchar
		);
	""")

	cursor.execute("""
		DROP TABLE IF EXISTS movieperson;
		CREATE TABLE movieperson (
			movie_id	integer references movie (movie_id) ON DELETE CASCADE,
			person_id	varchar references person (person_id) ON DELETE CASCADE,
			role		varchar,
			billing		integer,
			PRIMARY KEY (movie_id, person_id, role)
		);
	""")

	cursor.execute("""
		DROP TABLE IF EXISTS users CASCADE;
		CREATE TABLE users (
			user_id	integer PRIMARY KEY
		);
	""")

	cursor.execute("""
		DROP TABLE IF EXISTS usermovie;
		CREATE TABLE usermovie (
			user_id			integer references users (user_id) ON DELETE CASCADE,
			movie_id		integer references movie (movie_id) ON DELETE CASCADE,
			latest_rating	integer,
			PRIMARY KEY (user_id, movie_id)
		);
	""")

	cursor.execute("""
		DROP TABLE IF EXISTS review;
		CREATE TABLE review (
			viewing_id		integer PRIMARY KEY,
			user_id			integer references users (user_id) ON DELETE CASCADE,
			movie_id		integer references movie (movie_id) ON DELETE CASCADE,
			rating			integer,
			review_href		varchar UNIQUE
		);
	""")

	cursor.execute("""
		CREATE EXTENSION IF NOT EXISTS unaccent;
	""")

	conn.commit()

	cursor.close()
	conn.close()

def load_data_into_tables():
	"""
	Loads tables with initial data from CSVs

	Args: None
	Returns: None
	"""
	conn =  psycopg2.connect("dbname=letterboxddb")
	cursor = conn.cursor()

	dir_path = os.getcwd() + '/../data/'

	for table in ['movie', 'person', 'movieperson', 'users', 'usermovie', 'review']:
		copy_sql = "COPY {} FROM stdin DELIMITER ',' QUOTE '|' HEADER CSV;".format(table)

		with open(dir_path + '{}.csv'.format(table), 'r') as infile:
			cursor.copy_expert(sql=copy_sql, file=infile)
	
	conn.commit()

	cursor.close()
	conn.close()

if __name__ == "__main__":
	create_tables()
	load_data_into_tables()