import re
import requests
from bs4 import BeautifulSoup

class LetterboxdWebScraper:

	def __init__(self):
		pass

	def get_user_id(self, user):
		"""
		Retrieve user's numeric ID

		Args:
			user - string of Letterboxd username
		Returns: int user ID
		"""
		base_url = 'https://letterboxd.com/{}/'.format(user)
		base_url_text = requests.get(base_url).text
		soup = BeautifulSoup(base_url_text, 'html.parser')

		# there has got to be a less random way to grab this than from here
		return int(soup.find(attrs={'data-popmenu-id':True})['data-popmenu-id'].split('-')[-1])

	def get_watched_film_urls(self, user):
		"""
		Retrieve URLs for each page in a user's list of watched films ("Films" tab).

		Args:
			user - string of Letterboxd username
		Returns: list of URL strings
		"""
		base_url = 'https://letterboxd.com/{}/films/'.format(user)
		base_url_text = requests.get(base_url).text
		soup = BeautifulSoup(base_url_text, 'html.parser')

		# multiple pages of reviews
		try:
			final_page_num = int(soup.find(class_='pagination').find_all("a")[-1].string)
			return ['https://letterboxd.com/{}/films/page/{}/'.format(user, i) for i in range(1, final_page_num + 1)]

		# only one page of reviews
		except AttributeError:
			return [base_url]

	def get_review_urls(self, user):
		"""
		Retrieve URLs for each page in a user's list of reviews ("Reviews" tab).

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
		except AttributeError:
			return [base_url]

	def get_film_data(self, film_url):
		"""
		Retrieves data for a film.

		Args:
			film_url - URL of film's Letterboxd page
		Returns: dict of film data
		"""
		film_url_text = requests.get(film_url).text
		film_soup = BeautifulSoup(film_url_text, 'html.parser')

		wrapper_tag = film_soup.find('div', id='film-page-wrapper')

		movie_id = int(wrapper_tag.find(attrs={'data-film-id':True})['data-film-id'])
		name = wrapper_tag.find(attrs={'data-film-name':True})['data-film-name']
		year = int(wrapper_tag.find(attrs={'data-film-release-year':True})['data-film-release-year'])

		film_info = {
			'movie_id': movie_id,
			'name': name,
			'year': year,
			'cast_and_crew': []
		}

		# Add cast to film_info['cast_and_crew']
		cast_div = film_soup.find('div', id='tab-cast')
		if cast_div: # some films have no cast div (e.g. some documentaries)
			for cast_tag in cast_div.find_all('a', href=re.compile('/actor/')):
				film_info['cast_and_crew'].append(('actor', cast_tag['href'].split('/')[2], cast_tag.string))

		# Add crew to film_info['cast_and_crew']
		crew_roles = ['director', 'writer', 'editor', 'cinematography', 'composer']
		crew_div = film_soup.find('div', id='tab-crew')

		if crew_div: # some films have no crew div (e.g. "Toy Story 3: Na Moda com Ken!" (2010) (5 stars))
			for crew_role in crew_roles:
				for crew_tag in crew_div.find_all('a', href=re.compile('/{}/'.format(crew_role))):
					if crew_role == 'cinematography':
						film_info['cast_and_crew'].append(('cinematographer', crew_tag['href'].split('/')[2], crew_tag.string))
					else:
						film_info['cast_and_crew'].append((crew_role, crew_tag['href'].split('/')[2], crew_tag.string))
		
		return film_info

	def get_all_user_film_data(self, user):
		"""
		Retrieves data for all films watched by the given user, including latest rating.

		Args:
			user - string of Letterboxd username
		Returns: list of dicts of film data
		"""
		all_film_data = []

		for film_url in self.get_watched_film_urls(user):
			film_url_text = requests.get(film_url).text
			soup = BeautifulSoup(film_url_text, 'html.parser')

			for film_tag in soup.find_all('li', class_='poster-container'):
				# Used to retrieve film info
				film_url = 'https://letterboxd.com' + film_tag.find(attrs={'data-target-link':True})['data-target-link']

				film_data = self.get_film_data(film_url)
				
				# Need to collect ratings from user's Films page since a user may have rated a film without reviewing it
				try:
					rating = int(film_tag.find('span', class_='rating')['class'][-1].split('-')[-1])
				except TypeError:
					rating = None
				
				film_data['latest_rating'] = rating

				all_film_data.append(film_data)
			
		return all_film_data


	def get_all_user_review_data(self, user):
		"""
		Retrieves data for films reviewed by the given user.

		Args:
			user - string of Letterboxd username
		Returns: list of dicts of review data
		"""
		review_data = []

		for reviews_url in self.get_review_urls(user):
			review_url_text = requests.get(reviews_url).text
			soup = BeautifulSoup(review_url_text, 'html.parser')

			for film_tag in soup.find_all('li', class_='film-detail'):
				viewing_id = int(film_tag.find(attrs={'data-likeable-uid':True})['data-likeable-uid'].split(':')[-1])
				movie_id = int(film_tag.find(attrs={'data-film-id':True})['data-film-id'])
				try:
					rating = int(film_tag.find('span', class_='rating')['class'][-1].split('-')[-1])
				except TypeError:
					rating = None

				
				review_info = {
					'viewing_id': viewing_id,
					'movie_id': movie_id,
					'rating': rating
				}

				review_data.append(review_info)
		
		return review_data
