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