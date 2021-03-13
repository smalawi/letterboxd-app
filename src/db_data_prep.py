import os
import csv

from scraper import LetterboxdWebScraper

def write_init_csvs(user):
	"""
	Retrieves all user's Letterboxd data and writes the initial contents of each database table to CSVs

	Args:
		user - string of Letterboxd username
	Returns: None
	"""
	if not os.path.exists('../data'):
		os.mkdir('../data')

	dir_path = os.path.dirname(__file__) + '/../data/'

	scraper = LetterboxdWebScraper()

	user_id = scraper.get_user_id(user)
	all_film_data = scraper.get_all_user_film_data(user)
	all_review_data = scraper.get_all_user_review_data(user)

	with open(dir_path + 'user.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['user_id'])
		writer.writerow([user_id])

	movie_fieldnames = ['movie_id', 'name', 'year']

	with open(dir_path + 'movie.csv', 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=movie_fieldnames, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
		writer.writeheader()
		writer.writerows(all_film_data)

	usermovie_fieldnames = ['user_id', 'movie_id', 'latest_rating']
	usermovie_csv_data = [{'user_id': user_id, 'movie_id': f['movie_id'], 'latest_rating': f['latest_rating']} for f in all_film_data]
	
	with open(dir_path + 'usermovie.csv', 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=usermovie_fieldnames, delimiter=',')
		writer.writeheader()
		writer.writerows(usermovie_csv_data)
	
	person_fieldnames = ['person_id', 'name']
	person_csv_data = []

	movieperson_fieldnames = ['movie_id', 'person_id', 'role']
	movieperson_csv_data = []

	persons = set()

	for film in all_film_data:
		for role, person_id, person in film['cast_and_crew']:
			if person_id not in persons:
				persons.add(person_id)
				person_csv_data.append([person_id, person])
			movieperson_csv_data.append([film['movie_id'], person_id, role])
	
	with open(dir_path + 'person.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(person_fieldnames)
		writer.writerows(person_csv_data)

	with open(dir_path + 'movieperson.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(movieperson_fieldnames)
		writer.writerows(movieperson_csv_data)
	
	review_fieldnames = ['viewing_id', 'user_id', 'movie_id', 'rating']
	review_csv_data = [[r['viewing_id'], user_id, r['movie_id'], r['rating']] for r in all_review_data]

	with open(dir_path + 'review.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(review_fieldnames)
		writer.writerows(review_csv_data)


