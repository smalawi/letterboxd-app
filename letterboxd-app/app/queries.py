from unidecode import unidecode

from app.database import select

def search_for_movie(search_term):
	query = """
		SELECT
			m.movie_name,
			m.movie_href,
			b.person_name as director,
			um.latest_rating AS rating 
		FROM
			Movie m
		LEFT JOIN
			UserMovie um
		ON
			m.movie_id = um.movie_id
		LEFT JOIN (
			SELECT
				a.movie_id,
				p.person_name
			FROM (
				SELECT
					movie_id,
					MIN(person_id) AS person_id
				FROM
					MoviePerson
				WHERE
					role = 'director'
				GROUP BY movie_id
				) a
			LEFT JOIN
				Person p
			ON
				a.person_id = p.person_id
			) b
		ON
			m.movie_id = b.movie_id
		WHERE
			UPPER(unaccent(m.movie_name)) LIKE UPPER(unaccent('%{}%'))
		ORDER BY m.movie_name
		;
		""".format(search_term)
	results = select(query)
	
	return results

def search_for_person(search_term):
	query = """
		SELECT person_id, person_name, role, ct
		FROM
			(
			SELECT *, ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY ct DESC, role) rn
			FROM
				(
				SELECT
					p.person_id,
					p.person_name,
					mp.role,
					COUNT(*) AS ct
				FROM
					Person p
				LEFT JOIN
					MoviePerson mp
				ON
					p.person_id = mp.person_id
				WHERE
					p.person_id IN
						(
						SELECT person_id FROM Person
						WHERE UPPER(unaccent(person_name)) LIKE UPPER(unaccent('%{}%'))
						)
				GROUP BY p.person_id, p.person_name, mp.role
				) qt
			) rt
		WHERE rn = 1
		ORDER BY ct DESC
		;
		""".format(search_term)
	results = select(query)
	
	return results

def get_movie_info(movie_href):
	query = """
		SELECT
			m.*,
			um.latest_rating AS rating 
		FROM
			Movie m
		LEFT JOIN
			UserMovie um
		ON
			m.movie_id = um.movie_id
		WHERE m.movie_href = '{}';
		""".format(movie_href)
	results = select(query)
	
	return results[0]

def get_movie_persons(movie_href):
	query = """
		SELECT mp.*, p.person_name
		FROM MoviePerson mp
		LEFT JOIN Person p
		ON mp.person_id = p.person_id
		WHERE mp.movie_id IN
		(
			SELECT movie_id FROM Movie WHERE movie_href = '{}'
		)
		ORDER BY mp.role, mp.billing;
		""".format(movie_href)
	results = select(query)
	
	return results

def get_review_info(movie_href):
	query = """
		SELECT *
		FROM Review
		WHERE review_href LIKE '{}/%'
		ORDER BY viewing_date DESC;
		""".format(movie_href)
	results = select(query)
	
	return results

def get_person_name(person_id):
	query = """
		SELECT person_name FROM Person WHERE person_id = '{}';
		""".format(person_id)
	results = select(query)
	
	return results[0]['person_name']

def get_person_movies(person_id):
	query = """
		SELECT
			m.movie_name,
			m.year,
			m.movie_href,
			mp.role,
			um.latest_rating AS rating,
			m.movie_href
		FROM MoviePerson mp
		LEFT JOIN Movie m
		ON mp.movie_id = m.movie_id
		LEFT JOIN UserMovie um
		ON mp.movie_id = um.movie_id
		WHERE mp.person_id = '{}'
		ORDER BY mp.role, m.year, m.movie_name;
		""".format(person_id)
	results = select(query)
	
	return results