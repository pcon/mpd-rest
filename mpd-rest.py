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

import json
import sys
import os
import cherrypy

from mpd import MPDClient, CommandError

import mpdrest
from mpdrest.common import Config
from mpdrest.webserverInit import initWebServer

from lib.configobj import ConfigObj

initWebServer({
    'port': 8082,
    'host': '0.0.0.0',
    'web_root': '/',
    'damonize': False,
    'quiet': False,
})