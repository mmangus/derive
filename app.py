import random

from flask import Flask, render_template
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
    'dragging': False,
    'no_touch': True,
    'control_scale': True,
    'width': 75,
    'height': 60,
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
def play():
    placename, coordinates = random.choice(LOCATIONS)
    map = Map(
        location=coordinates,
        **DEFAULT_MAP_KWARGS
    )._repr_html_()
    return render_template('play.html', map=map, placename=placename)
