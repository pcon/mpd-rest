import json
import sys
import os
from mpd import MPDClient, CommandError
import cherrypy

def jsonify_tool_callback(*args, **kwargs):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    response.body = response.body

cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

def jpeg_tool_callback(*args, **kwargs):
    response = cherrypy.response
    response.headers['Content-Type'] = 'image/jpeg'
    response.body = response.body

cherrypy.tools.jpegify = cherrypy.Tool('before_finalize', jpeg_tool_callback, priority=30)

def mpdConnect(client, con_id):
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    try:
        client.password(secret)
    except CommandError:
        return False
    return True

def getImage(current):
    current = client.currentsong()
    folder = current['file'].rsplit('/', 2)

    path = MUSICROOT

    for part in folder[:len(folder)-1:]:
        path = path + '/' + part

        path = path + '/folder.jpg'

    return file(path, "rb").read()

HOST = 'localhost'
PORT = '6600'
PASSWORD = 'lamepassword'
MUSICROOT = '/export/music'
CON_ID = {'host': HOST, 'port': PORT}

client = MPDClient()
if not mpdConnect(client, CON_ID):
    print "Could not connect to mpd server"
    sys.exit(-1)

if PASSWORD != '':
    if not mpdAuth(client, PASSWORD):
        print "Invalid password"
        sys.exit(-1)

class StatusCover:


    @cherrypy.tools.jpegify()
    def index(self):
        return getImage(client.currentSong())
    index.exposed = True

class Status:
    cover = StatusCover()

    @cherrypy.tools.jsonify()
    def index(self):
        return json.dumps(client.status())
    index.exposed = True

class Root:
    status = Status()

    def index(self):
        return '<html>'+client.status()['state']+'</html>'
    index.exposed = True

config = {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8082,
}

cherrypy.config.update(config)
cherrypy.quickstart(Root())
