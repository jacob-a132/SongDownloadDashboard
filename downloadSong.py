import shutil
import os
import youtube_dlc
from shutil import copyfile
from mutagen.mp4 import MP4

ydl_opts = {
  'format':'bestaudio/best',
  'extractaudio':True,
  'audioformat':'m4a',
  'outtmpl':'song/%(track)s.%(ext)s',
  'noplaylist':True,
  'nocheckcertificate':True,
  'proxy':"",
  'addmetadata':True,
  'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'm4a',
    'preferredquality': '192',
  }, {
    'key': 'FFmpegMetadata'
  }]
}

localMusicFolder = "/Users/jacob/Documents/music/download/"
itunesAutoImportFolder = "/Users/jacob/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized/"

# copyToItunes = False

def addSong(url, artistOverride, albumOverride, copyToItunes):

  # download mp3
  with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
    try:
      info = ydl.extract_info(url)
    except Exception as e:
      return [1, e]
    videoTitle = info['title']
    songName = info['track'] or 'NA'
    meta = MP4("song/"+songName+'.m4a')
    meta['\xa9cmt'] = ''
    meta['\xa9day'] = meta['\xa9day'][0][0:4]
    if songName == 'NA':
      meta['\xa9ART'] = ''
    if artistOverride != '':
      meta['\xa9ART'] = artistOverride
    if albumOverride != '':
      meta['\xa9alb'] = albumOverride
    meta.save()
    fileName = songName + '.m4a'
    if songName == 'NA':
      os.rename("song/"+fileName,localMusicFolder+videoTitle+".m4a")
      fileName = videoTitle+".m4a"
    else:
      os.rename("song/"+fileName,localMusicFolder+fileName)
    if copyToItunes:
      copyfile(localMusicFolder+fileName,itunesAutoImportFolder+fileName)

  print("Completed successfully")
  return [0, fileName]


if __name__ == "__main__":
  url = 'https://www.youtube.com/watch?v=wW80mkZaYxY'
  with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
    pass
    ret = ydl.extract_info(url)
    name = ret['track']+'.m4a'
    print(ret['title'])
    meta = MP4("song/"+name)
    meta['\xa9cmt'] = ''
    meta['\xa9day'] = meta['\xa9day'][0][0:4]
    meta.save()