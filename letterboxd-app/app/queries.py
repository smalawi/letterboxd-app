from unidecode import unidecode

from app.database import select

def query_movie(search_term):
	query = """
		SELECT
			m.movie_name,
			um.latest_rating AS rating 
		FROM
			Movie m
		LEFT JOIN
			UserMovie um
		ON
			m.movie_id = um.movie_id
		WHERE
			UPPER(unaccent(m.movie_name)) LIKE UPPER(unaccent('%{}%'))
		ORDER BY m.movie_name
		;
		""".format(search_term)
	results = select(query)
	
	return results

def query_person(search_term):
	query = """
		SELECT person_name, role, ct
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