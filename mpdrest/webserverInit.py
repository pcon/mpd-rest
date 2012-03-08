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

#    app = cherrypy.tree.mount(WebInterface(), options['web_root'], config)
#    cherrypy.engine.start();
#    cherrypy.engine.block();

#    if hasattr(cherrypy.engine, 'signal_handler'):
        #if not options.quiet and not options.daemonize:
#        cherrypy.engine.signal_handler.set_handler(signal='SIGINT', listener=sys.exit)
#        cherrypy.engine.signal_handler.subscribe()

#    cherrypy.server.start()