from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import urllib
import time
import json
import downloadSong
import sys

hostName = ""
hostPort = 8080

addToItunes = False
if (len(sys.argv) == 2):
  addToItunes = True

class MyHandler(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_headers()
    # / -> index.html, /index.css -> index.css
    fileName = "index.html"
    if(self.path == "/index.css"): fileName = "index.css"
    f = open(fileName, 'rb')
    self.wfile.write(f.read())

  # POST is for submitting data.
  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length).decode("utf-8")
    request_data = json.loads(post_data)
    print('request received to download ' + request_data['url'])
    error, fileName = downloadSong.addSong(request_data['url'], request_data['artist'], request_data['album'], addToItunes) # calls other file
    self._set_headers()
    if(error):
      fileName = 'error occured'
    return self.wfile.write(json.dumps({'fileName': fileName, 'id': request_data['id']}).encode('utf-8'))

myServer = HTTPServer((hostName, hostPort), MyHandler)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
if(addToItunes):
  print('Adding to itunes')

try:
  myServer.serve_forever()
except KeyboardInterrupt:
  pass
