import random

from flask import (
    abort,
    Flask,
    redirect,
    render_template,
    url_for,
)
from flask_bootstrap import Bootstrap
from folium import Map

# TODO temporary, see locations.py
import locations
LOCATIONS = locations.load_from_disk()

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

@app.route('/')
def homepage():
    return render_template('home.html')


# @app.route('/play/')  TODO handle this later
@app.route('/play/<loc_id>/')
def play(loc_id=None):
    # TODO:
    #  - hook this up to a DB model
    #  - randomize ordering (or create sets??)
    #  - track session/user to prevent duplicates
    # 
    # if not loc_id:
    #    loc_id = random.choice(range(len(LOCATIONS)))
    #    return redirect(url_for('play', loc_id=loc_id))
    
    try:
        loc_id = int(loc_id)
    except ValueError:
        abort(400)
    _, coordinates = LOCATIONS[int(loc_id)]
    next_loc = loc_id + 1 if loc_id < len(LOCATIONS) else 0
    map = Map(
        location=coordinates,
        **DEFAULT_MAP_KWARGS
    )._repr_html_()  # TODO override to e.g. change placeholder etc

    return render_template('play.html', map=map, next_loc=next_loc)
