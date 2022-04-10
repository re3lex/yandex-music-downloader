import concurrent.futures
import configparser
from typing import List
import eyed3
import os.path
from yandex_music.client import Client
from yandex_music import Track
from components.fileLoader import FileLoader
from components.radio import Radio
from datetime import datetime

config = configparser.RawConfigParser()
config.read('config.properties')

BASE_PATH=config.get('Base', 'yam.dir')
station_id = config.get('Base', 'radio.stationId')

def downloadTrack(client: Client, track: Track) -> List['str']:
  global BASE_PATH
  loaded = []
  

  fl = FileLoader(BASE_PATH, track)
  print(f'\nChecking: {fl.getName()}')
  if not fl.isLoadNeeded():
    print(f'Track is skipped: {fl.getName()}')
    print(f'Skip request for {track.id}.')
    return loaded

  print(f'Loading: {fl.getName()}')
  print('Debug info: ',track)
  fl.load()

  print(f'Finished request for {track.id}.')

  loaded.append(fl.getName()+'\n'+fl.getTrackPath())
  return loaded



lastTrackIdFile = open(BASE_PATH+'.lastTrackId', 'r+')
lastTrackId = lastTrackIdFile.read()

token = ''
with open('.token', "r") as file:
    token = file.readline()

if token is None or token == '':
  raise ValueError('Token is not defined')

client = client = Client(token).init()

radio = Radio(client)

# start radio and get first track
radio.start_radio(station_id, None)

totalLoaded = []

for i in range(0, 100):
  timestamp = datetime.timestamp(datetime.now())
  next_track = radio.play_next()
  lastTrackId = next_track.id
  lastTrackIdFile.seek(0)
  lastTrackIdFile.write(lastTrackId)
  lastTrackIdFile.truncate()
  print('lastTrackId: '+lastTrackId)

  try:
    loaded = downloadTrack(client, next_track)
  except Exception as exc:
    print('Generated an exception: %s' % (exc))
  else:
    totalLoaded.extend(loaded)
    print('Loaded %d tracks' % (len(loaded)))

lastTrackIdFile.close()

print(f'\n-------------------------------------------\n')
print(f'Loaded: '+'\n---\n'.join(totalLoaded))
print(f'\n\nTotal loaded: {len(totalLoaded)}')
