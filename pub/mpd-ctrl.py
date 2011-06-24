#!/usr/bin/env python

import sys
import ConfigParser
import json
import cgitb
import os

from mpd import MPDClient, CommandError
from socket import error as SocketError

cgitb.enable()

config = ConfigParser.ConfigParser()
config.read('/usr/share/mpd-rest/mpd.conf')
HOST = config.get('mpd-server', 'server')
PORT = config.get('mpd-server', 'port')
PASSWORD = config.get('mpd-server', 'password')

CON_ID={'host': HOST, 'port':PORT}

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

def main():
    print "Content-Type: application/json\n"
    client = MPDClient()
    if not mpdConnect(client, CON_ID):
        print '{ "status": "failure", "message": "failed to connect to MPD server. '+HOST+':'+PORT+'"}'
        sys.exit(-1)

    if PASSWORD != '':
        if not mpdAuth(client, PASSWORD):
            print '{ "status": "failure", "message": "failed to auth against MPD server."}'
            sys.exit(-1)

    command = os.environ['SCRIPT_NAME'].replace('/mpd/control/', '')

    try:
        if command == 'pause/':
            client.pause()
            print '{ "status": "success" }'
        elif command == 'play/':
            client.play()
            print '{ "status": "success" }'
        elif command == 'next/':
            client.next()
            print '{ "status": "success" }'
        elif command == 'previous/':
            client.previous()
            print '{ "status": "success" }'
    except CommandError:
        print '{ "status": "failure", "message": "unknown commane" }'

if __name__ == "__main__":
    main()