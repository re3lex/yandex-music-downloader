import configparser
import sys
import concurrent.futures
from typing import List
import eyed3
import os.path
from yandex_music.client import Client
from yandex_music import Track
from components.fileLoader import FileLoader
from datetime import datetime

config = configparser.RawConfigParser()
config.read('config.properties')

BASE_PATH=config.get('Base', 'yam.dir')

print (BASE_PATH)

trackIds = [592649]

if len(sys.argv) > 1:
  trackIds = []
  for i in range(1, len(sys.argv)):
    trackIds.append(sys.argv[i])

token = ''
with open('.token', "r") as file:
    token = file.readline()

if token is None or token == '':
  raise ValueError('Token is not defined')

client = client = Client(token).init()

loaded = []
tracks = client.tracks(trackIds)

for t in tracks:
  fl = FileLoader(BASE_PATH, t)
  print(f'Checking: {fl.getName()}')
  if not fl.isLoadNeeded():
    print(f'Track is skipped: {fl.getName()}')
    continue

  print(f'Loading: {fl.getName()}')
  fl.load()
  loaded.append(fl.getName())

print(f'Loaded: \n'+'\n'.join(loaded))
print(f'Total loaded: {len(loaded)}')