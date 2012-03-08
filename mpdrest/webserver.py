# Copyright 2011 Patrick Connelly
#
# This file is part of mpd-rest
#
# mpd-rest is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import cherrypy.lib

from mpd import MPDClient, CommandError

import mpdrest
from mpdrest.mpdlib import MpdLib
from mpdrest.common import Config

try:
    import json
except ImportError:
    from lib import simplejson as json

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

class StatusCover:
    @cherrypy.expose
    @cherrypy.tools.jpegify()
    def index(self):
        return MpdLib.getImage(Config.client.currentsong())

class StatusSong:
    cover = StatusCover()

    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def json(self):
        return json.dumps(Config.client.currentsong())

    @cherrypy.expose
    def html(self):
        song = Config.client.currentsong()
        body = """<html><body><img src="cover" /><br/><p>%s</p><p>%s</p><p>%s</p>""" % (song['title'], song['artist'], song['album'], )
        return body

    @cherrypy.expose
    def index(self, format=None):
        if format == "json":
            return StatusSong.json(self)

        return StatusSong.html(self)

class StatusServer:
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def json(self):
        return json.dumps(Config.client.status())

    @cherrypy.expose
    def html(self):
        server = Config.client.status()
        return "<html><body>Server is currently: %s</body></html>" % (server['state'],)

    @cherrypy.expose
    def index(self, format=None):
        if format == "json":
            return StatusServer.json(self)

        return StatusServer.html(self)

class Status:
    song = StatusSong()
    server = StatusServer()

    @cherrypy.expose
    def index(self):
        return "<html><body><a href='server'>Server Status</a><br/><a href='song'>Song Status</a></body></html>"

class WebInterface:
    def __init__(self):
        Config.client = MPDClient()
        if not MpdLib.mpdConnect(Config.client):
            print "Could not connect to mpd server"
            sys.exit(-1)

    status = Status()

    @cherrypy.expose
    def index(self):
        return """<html><body><p><b>Status</b><ul><li><a href="status/server/">Server<a></li><li><a href="status/song/">Song</a></li></ul></p></body></html>"""