from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField

class ArtistForm(FlaskForm):
    name = StringField('Artist Name')
    genre = StringField('Genre')
    submit = SubmitField('Submit')

class ConcertForm(FlaskForm):
    artist = SelectField('Artist name')
    venue = StringField('Venue')
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')

class PlanConcertForm(FlaskForm):
    artist = SelectField('Artist name')
    city = SelectField('City')
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')