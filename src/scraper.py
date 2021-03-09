import re
import requests
from bs4 import BeautifulSoup

def get_review_urls(user):
	"""
	Retrieve URLs for each page in a user's list of reviews.

	Args:
		user - string of Letterboxd username
	Returns: list of URL strings
	"""
	base_url = 'https://letterboxd.com/{}/films/reviews/'.format(user)
	base_url_text = requests.get(base_url).text
	soup = BeautifulSoup(base_url_text, 'html.parser')

	# multiple pages of reviews
	try:
		final_page_num = int(soup.find(class_='pagination').find_all("a")[-1].string)
		return ['https://letterboxd.com/{}/films/reviews/page/{}/'.format(user, i) for i in range(1, final_page_num + 1)]

	# only one page of reviews
	except AttributeError as e:
		return [base_url]

def get_review_data(reviews_url):
	"""
	Retrieves data for films listed at the given webpage.

	Args:
		reviews_url - string of URL of a page of reviews
	Returns: dict of review and film data
	"""
	review_data = []

	review_url_text = requests.get(reviews_url).text
	soup = BeautifulSoup(review_url_text, 'html.parser')

	film_tags = soup.find_all('li', class_='film-detail')

	for film_tag in film_tags:
		# Info that can be retrieved from review list webpage
		name = film_tag.find('a', href=re.compile('/film/')).string
		year = int(film_tag.find('a', href=re.compile('/films/year')).string)
		try:
			rating = int(film_tag.find('span', class_='rating')['class'][-1].split('-')[-1])
		except TypeError as ex:
			rating = None

		# For info to be retrieved from film's dedicated webpage
		name_for_url = film_tag.find('a', href=re.compile('/film/'))['href'].split('/')[3]
		
		film_info = {
			'name': name,
			'id': name_for_url,
			'year': year,
			'rating': rating
		}

		film_url = 'https://letterboxd.com/film/{}/'.format(name_for_url)
		film_url_text = requests.get(film_url).text
		film_soup = BeautifulSoup(film_url_text, 'html.parser')

		# Cast list
		film_info['cast'] = []
		cast_div = film_soup.find('div', id='tab-cast')
		if cast_div: # some films have no cast div (e.g. some documentaries)
			for cast_tag in cast_div.find_all('a', href=re.compile('/actor/')):
				film_info['cast'].append((cast_tag['href'].split('/')[2], cast_tag.string))

		# Crew lists
		crew_roles = ['director', 'writer', 'editor', 'cinematography', 'composer']
		crew_div = film_soup.find('div', id='tab-crew')

		for crew_role in crew_roles:
			film_info[crew_role] = []
			for crew_tag in crew_div.find_all('a', href=re.compile('/{}/'.format(crew_role))):
				film_info[crew_role].append((crew_tag['href'].split('/')[2], crew_tag.string))

		review_data.append(film_info)
	
	return review_data
