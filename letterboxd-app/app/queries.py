from unidecode import unidecode

from app.database import select

def query_movie(search_term):
	query = """
		SELECT m.movie_name, um.latest_rating AS rating 
		FROM Movie m LEFT JOIN UserMovie um
		ON m.movie_id = um.movie_id
		WHERE UPPER(unaccent(m.movie_name)) LIKE UPPER(unaccent('%{}%'));
		""".format(search_term)
	results = select(query)
	
	return results