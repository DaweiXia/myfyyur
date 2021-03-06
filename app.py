#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import time
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from models import *
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en_US')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  data = []
  for venue in venues:
    venue_item = {}
    venue_item['id'] = venue.id
    venue_item['name'] = venue.name
    venue_item['num_upcoming_shows'] = db.session.query(Show).filter(Show.venue_id==venue.id,
    Show.start_time>time.strftime('%Y-%m-%d %H:%M:%S')).count()
    if data:
      for item in data:
        if item['city'] == venue.city and item['state'] == venue.state:
          item['venues'].append(venue_item)
    else:
      item = {}
      item['city'] = venue.city
      item['state'] = venue.state
      item['venues'] = []
      item['venues'].append(venue_item)
      data.append(item)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.like('%'+search_term+'%')).all()
  data = []
  for venue in venues:
    item = {}
    item['id'] = venue.id
    item['name'] = venue.name
    num = Show.query.filter(Show.venue_id == venue.id,
    Show.start_time > time.strftime('%Y-%m-%d %H:%M:%S')).count()
    item['num_upcoming_shows'] = num
    data.append(item)

  response = {
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  past_shows = Show.query.join(Artist) \
                         .filter(Show.venue_id == venue_id,
                         Show.start_time < time.strftime('%Y-%m-%d %H:%M:%S')) \
                         .all()
  data.past_shows = past_shows
  upcoming_shows = Show.query.join(Artist) \
                             .filter(Show.venue_id == venue_id,
                             Show.start_time > time.strftime('%Y-%m-%d %H:%M:%S')) \
                             .all()
  data.upcoming_shows = upcoming_shows
  data.past_shows_count = len(data.past_shows)
  data.upcomint_shows_count = len(data.upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website = request.form.get('website')
  seeking_talent = True if request.form.get('seeking_talent') else False
  seeking_description = request.form.get('seeking_description')
  
  try:
    venue = Venue(name=name, city=city, state=state, address=address,
    phone=phone, genres=genres, facebook_link=facebook_link,
    image_link=image_link, website=website, seeking_talent=seeking_talent,
    seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.like('%'+search_term+'%')).all()
  data = []
  for artist in artists:
    item = {}
    item['id'] = artist.id
    item['name'] = artist.name
    num = Show.query.filter(Show.artist_id == artist.id,
    Show.start_time > time.strftime('%Y-%m-%d %H:%M:%S')).count()
    item['num_upcoming_shows'] = num
  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  data = Artist.query.get(artist_id)
  past_shows = Show.query.join(Venue) \
                         .filter(Show.artist_id == artist_id,\
                         Show.start_time < time.strftime('%Y-%m-%d %H:%M:%S')) \
                         .all()
  data.past_shows = past_shows
  upcoming_shows = Show.query.join(Venue) \
                             .filter(Show.artist_id == artist_id, \
                             Show.start_time > time.strftime('%Y-%m-%d %H:%M:%S')) \
                             .all()
  data.upcoming_shows = upcoming_shows
  data.past_shows_count = len(data.past_shows)
  data.upcoming_shows_count = len(data.upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website = request.form.get('website')
  seeking_venue = True if request.form.get('seeking_venue') else False
  seeking_description = request.form.get('seeking_description')

  try:
    artist = Artist(name=name, city=city, state=state, phone=phone,
    genres=genres, facebook_link=facebook_link, image_link=image_link,
    website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
    db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = []
  shows = Show.query.all()
  for show in shows:
    item = {}
    item['venue_id'] = show.venue_id
    item['venue_name'] = Venue.query.get(show.venue_id).name
    item['artist_id'] = show.artist_id
    item['artist_name'] = Artist.query.get(show.artist_id).name
    item['artist_image_link'] = Artist.query.get(show.artist_id).image_link
    item['start_time'] = dateutil.parser.parse(str(show.start_time))
    data.append(item)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  try:
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
