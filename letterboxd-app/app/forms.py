from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
	query_type = SelectField('Select one',
		choices=[('', 'Select one'), ('movie', 'Movie'), ('person', 'Person')],
		validators=[DataRequired('Please select an option from the dropdown.')])
	search_term = StringField('Search term',
		validators=[DataRequired('Please enter a search term.')])
	submit = SubmitField('Submit')