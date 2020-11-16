import os
import zipfile

import pandas as pd
import requests

from io import BytesIO

# TODO:
#  - make a DB model for this
#  - store "hints" - hemisphere, country, parent admX?
#  - dynamically set zoom level by city bounding box?

GEONAMES_COLUMNS = [
  'geonameid',
  'name',
  'asciiname',
  'alternatenames',
  'latitude',
  'longitude',
  'feature class',
  'feature code',
  'country code',
  'cc2',
  'admin1 code',
  'admin2 code',
  'admin3 code',
  'admin4 code',
  'population',
  'elevation',
  'dem',
  'timezone',
  'modification date',
]

def geonames_to_file(n=100):
    geonames_dumpfile = BytesIO(
        requests.get(
            "http://download.geonames.org/export/dump/cities15000.zip"
        ).content
    )
    cities = zipfile.ZipFile(geonames_dumpfile).open("cities15000.txt") 
    cities_df = pd.read_csv(cities, sep='\t', names=GEONAMES_COLUMNS)
    cities_df['coordinates'] = cities_df[['latitude', 'longitude']].values.tolist()
    top_n = cities_df.sort_values('population', ascending=False)[[
        'name', 'coordinates'
    ]][:n].to_json('cities.json')


def load():
    if not os.path.exists("cities.json"):
        geonames_to_file()
    # could just use json module but we've got pandas imported already
    return pd.read_json("cities.json").values
