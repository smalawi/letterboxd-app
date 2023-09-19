The app is up and running for my Letterboxd account [here](https://letterboxd-app.fly.dev), hosted on [fly.io](https://fly.io).

# Intro

[Letterboxd](https://letterboxd.com) is a site for logging movies and sharing thoughts on them. The social networking aspect is a strong differentiator between Letterboxd and alternative sites/methods for logging film viewings. But interfacing with one's own watch data can be a cumbersome process, entailing menu diving and hovering over / clicking on icons of posters.

The Flask app in this repo queries a user's Letterboxd viewing and review data and aims to present it in a way that makes it simpler to answer questions like "what ratings have I given to movies directed by Claire Denis?" or "what are my favorite movies with Morricone soundtracks?"

Since Letterboxd doesn't have a public API (it's in a closed beta), all data currently must be webscraped. The app is designed to connect to a Postgres database populated with user data. Scripts for these tasks are also provided in this repo.

# Usage

The app can be run locally with `flask run`, or deployed somewhere. I used to host it on Heroku, with RDS for data store, but Heroku got rid of their free tier so I moved both the app and database to fly.io :)

The nested `letterboxd-app` folder is the Flask application directory. Webscraping + database prep code lives in the `src` folder.

Dependencies (for the Flask app as well as the scraping/database code) are listed in `letterboxd-app/requirements.txt`

See `env.sample.txt` for instructions on configuring the database connection.
