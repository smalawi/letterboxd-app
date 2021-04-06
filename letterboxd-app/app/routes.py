from flask import render_template, flash, redirect, url_for, session

from app import app
from app.forms import QueryForm
from app.queries import search_for_movie, search_for_person, get_movie_info, get_movie_persons, get_person_name, get_person_movies

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = QueryForm()
	
	results = []
	results_type = ''
	search_term = ''

	"""
	if 'query_results' in session:
		results = session['query_results']
		results_type = session['results_type']
		session.pop('query_results')
		session.pop('results_type')
	"""

	if form.validate_on_submit():
		#flash('query_type {}, search term {}'.format(form.query_type.data, form.search_term.data))
		if form.query_type.data == 'movie':
			"""
			session['results_type'] = 'movie'
			session['query_results'] = query_movie(form.search_term.data)
			"""
			results_type = 'movie'
			search_term = form.search_term.data
			results = search_for_movie(search_term)
		elif form.query_type.data == 'person':
			results_type = 'person'
			search_term = form.search_term.data
			results = search_for_person(search_term)
		form.search_term.data = ''
		#return redirect(url_for('index'))
	return render_template('index.html', form=form, search_term=search_term, results=results, results_type=results_type)

@app.route('/movie/<movie_href>')
def movie(movie_href):
	movie_info = get_movie_info(movie_href)
	movieperson_info = get_movie_persons(movie_href)

	ref = {
		'actor':			1,
		'director':			2, 
		'writer':			3,
		'editor':			4,
		'cinematographer':	5,
		'composer': 		6
	}
	sorted_movieperson_info = sorted(movieperson_info, key=lambda x: ref[x['role']])

	cast_count = len([c for c in movieperson_info if c['role'] == 'actor'])

	return render_template('movie.html', movie_href=movie_href, movie_info=movie_info, movieperson_info=sorted_movieperson_info, cast_count=cast_count)

@app.route('/person/<person_id>')
def person(person_id):
	person_name = get_person_name(person_id)
	person_movies_info = get_person_movies(person_id)

	all_credits = [m['role'] for m in person_movies_info]
	unique_roles = list(set(all_credits))
	most_common_role = max(set(all_credits), key=all_credits.count)

	# for writer-directors - probably should have default role of director
	if all_credits.count(most_common_role) == all_credits.count('director'):
		most_common_role = 'director'

	# place most common role at beginning of list for default dropdown value
	mcr_idx = unique_roles.index(most_common_role)
	temp = unique_roles[mcr_idx]
	unique_roles[mcr_idx] = unique_roles[0]
	unique_roles[0] = temp

	return render_template('person.html',
								person_id=person_id,
								person_name=person_name,
								person_movies_info=person_movies_info,
								unique_roles=unique_roles)
