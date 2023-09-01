# Intro
This app lived [here](https://letterboxd-client.herokuapp.com/index), but is offline for the time being on account of Heroku eliminating its free tier.

The nested `letterboxd-app` folder is the Flask application directory.

Dependencies (for the Flask app as well as the scraping/database code) are listed in `letterboxd-app/requirements.txt`

See `env.sample.txt` for instructions on configuring the database connection.

Heroku deployment (after configuring Heroku remote): `git subtree push --prefix letterboxd-app heroku main`
