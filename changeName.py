import os
import sys
from mutagen.mp4 import MP4
from mutagen.mp3 import EasyMP3 as MP3
import argparse
parser = argparse.ArgumentParser()

def changeName():

  #-d <directory> -ar <artist> -al <album>
  parser.add_argument("-d", "--directory", help="Directory")
  parser.add_argument("-ar", "--artist", help="Artist name")
  parser.add_argument("-al", "--album", help="Album name")
  args = parser.parse_args()

  if (args.directory == None or args.artist == None or args.album == None):
    print('USAGE: python3 changeName.py -d <directory> -ar <artist> -al <album>')
    return

  directory = args.directory
  songsUpdated = 0
  source = os.listdir(directory)

  for songName in source:
    if songName.endswith(".m4a"):
      meta = MP4(directory+'/'+songName)
      meta['\xa9nam'] = songName[:songName.index('.m4a')]
      meta['\xa9ART'] = args.artist
      meta['\xa9alb'] = args.album
      meta.save()
      songsUpdated += 1
    if songName.endswith(".mp3"):
      meta = MP3(directory+'/'+songName)
      meta['title'] = songName[:songName.index('.mp3')]
      meta['artist'] = args.artist
      meta['album'] = args.album
      meta.save()
      songsUpdated += 1

changeName()