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

import cherrypy
import os.path
import sys

import mpdrest
from mpdrest.webserver import WebInterface

def initWebServer(options = {}):
    options.setdefault('port', 8080)
    options.setdefault('host', '0.0.0.0')
    options.setdefault('web_root', '/')
    options.setdefault('quiet', False)
    options.setdefault('daemonize', False)

    assert isinstance(options['port'], int)

    options_dict = {
        'server.socket_port': options['port'],
        'server.socket_host': options['host'],
    }

    cherrypy.config.update(options_dict)

    config = {}

    cherrypy.quickstart(WebInterface(), options['web_root'], config)