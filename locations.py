from io import BytesIO
import os
import zipfile

from iso3166 import countries
import pandas as pd
import requests

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


def cc_to_name(cc):
  try:
    country = countries.get(cc)
  except KeyError:
    return 'Geonames value was not a ISO 3166 country code'
  return country.apolitical_name


def geonames_to_file(n=100):
    geonames_dumpfile = BytesIO(
        requests.get(
            "http://download.geonames.org/export/dump/cities15000.zip"
        ).content
    )
    cities = zipfile.ZipFile(geonames_dumpfile).open("cities15000.txt") 
    cities_df = pd.read_csv(cities, sep='\t', names=GEONAMES_COLUMNS)
    cities_df["coordinates"] = cities_df[["latitude", "longitude"]].values.tolist()
    cities_df["continent_or_ocean"] = cities_df["timezone"].apply(lambda tz: tz.split("/")[0])
    # TODO fuzzy reckoning on hemispheres; what"s the lon equivalent of "equatorial?"
    cities_df["hemisphere_lat"] = cities_df["latitude"].apply(lambda lat: "North" if lat >= 0 else "South")
    cities_df["hemisphere_lon"] = cities_df["longitude"].apply(lambda lon: "East" if lon >= 0 else "West")
    cities_df["country_name"] = cities_df["country code"].apply(lambda cc: cc_to_name(cc))
    top_n = cities_df.sort_values("population", ascending=False)[[
        "name", "coordinates", "continent_or_ocean", "hemisphere_lat", "hemisphere_lon", "country_name"
    ]][:n].to_json("cities.json")


def load():
    if not os.path.exists("cities.json"):
        geonames_to_file()
    # could just use json module but we've got pandas imported already
    cities_df = pd.read_json("cities.json")
    return cities_df.to_records()