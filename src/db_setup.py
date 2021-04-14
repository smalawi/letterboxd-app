import os
import sys
import psycopg2
from dotenv import load_dotenv

def get_connection(local_flag):
	"""
	Creates connection to Postgres database

	Args:
		local_flag - '-l' or '-local' to setup local db rather than RDS
	Returns: psycopg2 connection to database
	"""

	load_dotenv()

	if local_flag:
		conn = psycopg2.connect(database=os.environ.get('LOCAL_BOXD_DB_NAME'))
	else:
		conn = psycopg2.connect(
			database=os.environ.get('BOXD_DB_NAME'),
			user=os.environ.get('BOXD_DB_USER'),
			password=os.environ.get('BOXD_DB_PASSWORD'),
			host=os.environ.get('BOXD_DB_HOST'),
			port=os.environ.get('BOXD_DB_PORT')
		)
	
	return conn

def create_tables(conn):
	"""
	Creates tables in database

	Args:
		conn - psycopg2 connection to database
	Returns: None
	"""

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
			viewing_date	date,
			rating			integer,
			review_href		varchar UNIQUE
		);
	""")

	cursor.execute("""
		CREATE EXTENSION IF NOT EXISTS unaccent;
	""")

	conn.commit()

	cursor.close()

def load_data_into_tables(conn):
	"""
	Loads tables with initial data from CSVs

	Args:
		conn - psycopg2 connection to database
	Returns: None
	"""

	cursor = conn.cursor()

	dir_path = os.getcwd() + '/../data/'

	for table in ['movie', 'person', 'movieperson', 'users', 'usermovie', 'review']:
		copy_sql = "COPY {} FROM stdin DELIMITER ',' QUOTE '|' HEADER CSV;".format(table)

		with open(dir_path + '{}.csv'.format(table), 'r') as infile:
			cursor.copy_expert(sql=copy_sql, file=infile)
	
	conn.commit()

	cursor.close()

if __name__ == "__main__":
	try:
		flag = sys.argv[1]
	except IndexError:
		flag = ''
	
	if flag and flag not in ['-l', '--local']:
		print("Unknown flag {} - use -l or --local to populate local db".format(flag))
		sys.exit(1)

	conn = get_connection(flag)

	try:
		create_tables(conn)
		load_data_into_tables(conn)
	except Exception as e:
		print(e)

	conn.close()