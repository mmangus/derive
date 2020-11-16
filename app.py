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

import locations

# TODO temporary, see locations.py
LOCATIONS = locations.load()
DEFAULT_MAP_KWARGS = {
    "tiles": "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png",
    "attr": "Map tiles by <a href='http://stamen.com'>Stamen Design</a>, <a href="
            "'http://creativecommons.org/licenses/by/3.0'>CC BY 3.0</a> &mdash; Map data &copy;"
            " <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors.",
    "zoom_control": False,
    "scrollWheelZoom": False,
    "doubleClickZoom": False,
    "dragging": False,
    "no_touch": True,
    "control_scale": True,
    "width": "100",
    "height": "100",
}

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/play/")
@app.route("/play/<loc_id>/")
def play(loc_id=None):
    # TODO:
    #  - hook this up to a DB model
    #  - randomize ordering (or create sets??)
    #  - track session/user to prevent duplicates
    if not loc_id:
       loc_id = random.choice(range(len(LOCATIONS)))
       return redirect(url_for("play", loc_id=loc_id))
    
    try:
        loc_id = int(loc_id)
    except ValueError:
        abort(400)
    place_data  = LOCATIONS[int(loc_id)]
    place_name = place_data.name
    hints = [
        ("Hemisphere (latitude)", place_data.hemisphere_lat),
        ("Hemisphere (longitude)", place_data.hemisphere_lon),
        ("Continent (ocean for islands)", place_data.continent_or_ocean),
        ("Country", place_data.country_name),
    ]
    next_loc = loc_id + 1 if loc_id < len(LOCATIONS) else 0
    map = Map(
        location=place_data.coordinates,
        **DEFAULT_MAP_KWARGS
    )._repr_html_()  # TODO override to e.g. change placeholder etc

    return render_template(
        "play.html",
        map=map,
        next_loc=next_loc,
        placen_name=place_name,
        hints=hints,
    )
