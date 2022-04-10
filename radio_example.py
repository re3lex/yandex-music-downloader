from math import floor
from random import random
from time import sleep

from yandex_music import Client

from components.radio import Radio

token = ''
with open('.token', "r") as file:
    token = file.readline()

if token is None or token == '':
  raise ValueError('Toke is not defined')

# API instance
client = client = Client(token).init()

# Get random station
#_stations = client.rotor_stations_list()
#_station_random_index = floor(len(_stations) * random())
#_station = _stations[_station_random_index].station
_station_id = 'user:test_user'
#_station_from = _station.id_for_from
_station_from = None

# Radio instance
radio = Radio(client)

# start radio and get first track
radio.start_radio(_station_id, _station_from)
# print("[Radio] First track is:", first_track)

# get new track every 5 sec
while True:
  sleep(5)
  next_track = radio.play_next()
  artist = ', '.join(a.name for a in next_track.artists)
  title = next_track.title

  print(artist, " - ", title)