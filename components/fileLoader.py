from typing import Optional
import urllib.request
from typing import List
import eyed3
import os.path
from eyed3.id3 import Tag
import time

from yandex_music import Track


class FileLoader():
  def __init__(self, baseDir: str, track: Track):
    self.track = track
    self.baseDir = baseDir
    self.excludedDirChars = "<>:\"/\|?*."
    self.excludedFileChars = "<>:\"/\|?*"
    self.trackPath = None
    self.tag = None

  def getCoverUrl(self):
    return self.track.cover_uri.replace("%%", '200x200')

  def addCover(self, tag: Tag):
    url = self.getCoverUrl()
    resp = urllib.request.urlopen('https://'+url)
    data = resp.read()
    tag.images.set(3, data, 'image/jpeg')


  def getSafeFileName(self, s: str)->str:
    return ''.join(c for c in s if c not in self.excludedFileChars)

  def getSafeDirName(self, s: str)->str:
    return ''.join(c for c in s if c not in self.excludedDirChars).strip()

  def getTrackDir(self):
    artist = self.track.artists[0]
    album = self.track.albums[0] if len(self.track.albums) > 0 else None
    albumTitle = album.title if album else 'None'
    albumName = self.getSafeDirName(albumTitle)
    artistName = self.getSafeDirName(artist.name)
    return self.baseDir+artistName+'/'+albumName

  def getArtists(self):
    s = ', '.join(a.name for a in self.track.artists)
    return self.getSafeFileName(s)

  def getName(self):
    s = self.getArtists() + ' - '+ self.track.title + '.mp3'
    return self.getSafeFileName(s)

  def addTrackInfo(self, tag: Tag):
    t = self.track
    title = t.title

    allArtists = self.getArtists()
    album = t.albums[0]
    albumName = album.title

    tag.artist = allArtists
    tag.album = albumName
    tag.title = title
    self.addGenre(tag)
    

  def isLoadNeeded(self)-> bool:
    name = self.getName()
    trackDir = self.getTrackDir()
    path = trackDir+'/'+name

    if not self.track.available and not self.track.available_for_premium_users:
      print(f'Track {name} not available')
      return False

    if os.path.isfile(path):
      tag = self.getTag()
      self.addGenre(tag)
      self.addTrackId(tag, True)
      return False
    return True

  def addGenre(self, tag: Tag):
    album = self.track.albums[0]
    tag.genre = album.genre

  def addTrackId(self, tag: Tag, save: bool=False):
    tIds = tag.track_num

    if tIds[0] is None:
      aId = self.track.albums[0].id
      tag.track_num = (aId, self.track.id)
      if save is True:
        tag.save()

  def getTrackPath(self):
    if self.trackPath is None:
      name = self.getName()
      trackDir = self.getTrackDir()
      self.trackPath = trackDir+'/'+name
    return self.trackPath

  def load(self)->bool:
    if not self.isLoadNeeded() :
      return False
    
    trackDir = self.getTrackDir()

    if not os.path.isdir(trackDir):
      os.makedirs(trackDir)
      if not os.path.isdir(trackDir):
        raise ValueError(f'Cannot create dir {trackDir}')
    
    path = self.getTrackPath()
    try:
      self.track.download(filename=path, codec='mp3', bitrate_in_kbps=320)
    except Exception:
      self.track.download(filename=path, codec='mp3', bitrate_in_kbps=192)
    
    tag = self.getTag()
    self.addTrackInfo(tag)
    self.addTrackId(tag)
    self.addCover(tag)
    tag.save()
  
  def getTag(self):
    if self.tag is None:
      path = self.getTrackPath()
      audiofile = eyed3.load(path, tag_version=eyed3.id3.ID3_V2_3)
      if (audiofile.tag == None):
        audiofile.initTag(version=eyed3.id3.ID3_V2_3)
      self.tag = audiofile.tag
    return self.tag


if __name__ == '__main__':
  url = 'http://avatars.yandex.net/get-music-content/28589/46c1042d.a.61960-2/200x200'
  path = 'g:/yam/Дискотека Авария/Маньяки/tmp.mp3'

  audiofile = eyed3.load(path, tag_version=eyed3.id3.ID3_V2_3)
  if (audiofile.tag == None):
      audiofile.initTag(version=eyed3.id3.ID3_V2_3)
  tag = audiofile.tag
  # tag.artist = allArtists
  # tag.album = albumName
  # tag.title = title
  # tag.save()
  # cls = FileLoader(url=url, tag=tag)
  # cls.save()
