from flask import Flask, render_template, redirect, url_for, abort
from forms import ArtistForm, ConcertForm
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

artists = []
concerts = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/artists')
def favorite_artists():
    return render_template('artists.html', artists=artists)

@app.route('/artists/add', methods=['GET', 'POST'])
def add_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        artists.append({'name': form.name.data, 'genre': form.genre.data})
        return redirect(url_for('favorite_artists'))
    return render_template('add_artist.html', form=form)

@app.route('/artists/<int:artist_id>')
def artist_detail(artist_id):
    if artist_id >= len(artists):
        abort(404)

    artist = artists[artist_id]

    try:
        response = requests.get(
            "http://localhost:8003/artist_bio",
            params={"artist": artist['name']}
        )
        artist['bio'] = response.json().get("artist_bio")
    except requests.RequestException:
        artist['bio'] = None

    try:
        response = requests.get(
            "http://localhost:8004/top_songs",
            params={"artist": artist['name']}
        )
        artist['top_songs'] = response.json().get("top_songs")
    except requests.RequestException:
        artist['top_songs'] = None

    return render_template('artist_detail.html', artist=artist)

@app.route('/concerts')
def view_concerts():
    return render_template('concerts.html', concerts=concerts)

@app.route('/concerts/add', methods=['GET', 'POST'])
def log_concert():
    form = ConcertForm()
    choices = []
    for artist in artists:
        choices.append((artist['name'], artist['name']))
    form.artist.choices = choices
    if form.validate_on_submit():
        concerts.append({'artist': form.artist.data, 'venue': form.venue.data, 'date': form.date.data })
        return redirect(url_for('view_concerts'))                         
    return render_template('log_concert.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)