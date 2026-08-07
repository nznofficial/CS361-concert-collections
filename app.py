from flask import Flask, render_template, redirect, url_for, abort, request
from forms import ArtistForm, ConcertForm, PlanConcertForm
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

artists = []
concerts = []
cities = {
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Las Vegas': (36.1699, -115.1398),
    'Chicago': (41.8781, -87.6298),
    'Corvallis': (44.5646, -123.2620),
}

def convert_temp(value):
    response = requests.get(
        "http://localhost:8006/convert",
        params={"value": value, "from_unit": "F", "to_unit": "C"},
    )
    return response.json()["converted_value"]

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
            "http://localhost:8005/artist_bio",
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
        concerts.append({'artist': form.artist.data, 'city': form.city.data, 'date': form.date.data })
        return redirect(url_for('view_concerts'))                         
    return render_template('log_concert.html', form=form)

@app.route('/plans')
def view_plans():
    units = request.args.get('units', 'F')

    try:
        response = requests.get("http://localhost:8003/tasks")
        plans = response.json().get("tasks", [])
    except requests.RequestException:
        plans = []

    for plan in plans:
        plan['temp_hi'] = None
        plan['temp_lo'] = None

        coords = cities.get(plan['description'])
        if not coords:
            continue
        lat, lon = coords
        try:
            response = requests.get(
                "http://localhost:8002/forecast",
                params={"lat": lat, "lon": lon, "date": plan['due_date']}
            )
            data = response.json()
            plan['temp_hi'] = data.get('temp_max_f')
            plan['temp_lo'] = data.get('temp_min_f')
        except requests.RequestException:
            pass

        if units == 'C' and plan['temp_hi'] is not None:
            try:
                plan['temp_hi'] = convert_temp(plan['temp_hi'])
                plan['temp_lo'] = convert_temp(plan['temp_lo'])
            except requests.RequestException:
                pass

    return render_template('plans.html', plans=plans, units=units)

@app.route('/plan_concert', methods=['GET', 'POST'])
def plan_concerts():
    form = PlanConcertForm()
    form.artist.choices = [(a['name'], a['name']) for a in artists]
    form.city.choices = [(c, c) for c in cities]

    if form.validate_on_submit():
        requests.post(
            "http://localhost:8003/tasks",
            json={
                "title": form.artist.data,
                "description": form.city.data,
                "due_date": form.date.data.isoformat(),
                "status": "not_started",
                "priority": "medium",
            },
        )
        return redirect(url_for('view_plans'))

    return render_template('plan_concert.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)