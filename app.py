import random

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from folium import Map

app = Flask(__name__)
Bootstrap(app)

DEFAULT_MAP_KWARGS = {
    'tiles': "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png",
    'attr': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href='
            '"http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy;'
            ' <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors.',
    'zoom_control': False,
    'scrollWheelZoom': False,
    'doubleClickZoom': False,
    'dragging': False,
    'no_touch': True,
    'control_scale': True,
    'width': '100',
    'height': '100',
}

# TODO:
#  - make a DB model for this
#  - pull geonames data for global cities
#  - store "hints" - hemisphere, country, parent admX?
#  - dynamically set zoom level by city bounding box?
LOCATIONS = [
    ("San Francisco", [37.76, -122.44]),
    ("Portland", [45.52, -122.68]),
]


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/play/')
@app.route('/play/<loc_id>/')
def play(loc_id=None):
    if not loc_id:
        # TODO:
        #  - hook this up to a DB model
        #  - track session/user to prevent duplicates
        loc_id = random.choice(range(len(LOCATIONS)))
        return redirect(url_for('play', loc_id=loc_id))
    
    placename, coordinates = LOCATIONS[loc_id]
    map = Map(
        location=coordinates,
        **DEFAULT_MAP_KWARGS
    )._repr_html_()  # TODO override to e.g. change placeholder etc

    return render_template('play.html', map=map, placename=placename)
