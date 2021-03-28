from flask import render_template, flash, redirect, url_for, session

from app import app
from app.forms import QueryForm
from app.queries import query_movie, query_person

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
			results = query_movie(search_term)
		elif form.query_type.data == 'person':
			results_type = 'person'
			search_term = form.search_term.data
			results = query_person(search_term)
		form.search_term.data = ''
		#return redirect(url_for('index'))
	return render_template('index.html', form=form, search_term=search_term, results=results, results_type=results_type)