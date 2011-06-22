#!/usr/bin/env python

import sys
import ConfigParser
import json
import cgitb
import os

from mpd import MPDClient, CommandError
from socket import error as SocketError

ext2conttype = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif"}

cgitb.enable()

config = ConfigParser.ConfigParser()
config.read('/usr/share/mpd-rest/mpd.conf')
HOST = config.get('mpd-server', 'server')
PORT = config.get('mpd-server', 'port')
PASSWORD = config.get('mpd-server', 'password')
MUSICROOT = config.get('music', 'music-root')

CON_ID={'host': HOST, 'port':PORT}

def printStatus(status, message):
    print "Content-Type: application/json\n"
    print '{ "status": "'+status+'", "message": "'+message+'"}'

def dumpClientObject(obj):
    print "Content-Type: application/json\n"
    print json.dumps(obj)

def getCoverImage(client):
    print 'Content-Type: image/jpeg\n'
    current = client.currentsong()
    folder = current['file'].rsplit('/', 2)

    path = MUSICROOT

    for part in folder[:len(folder)-1:]:
        path = path + '/' + part

    #for now just grab folder.jpg
    path = path + '/folder.jpg'

    print file(path, "rb").read()

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
    client = MPDClient()
    if not mpdConnect(client, CON_ID):
        printStatus('failure', 'unable to connect to MPD Sever '+HOST+':'+PORT)
        sys.exit(-1)

    if PASSWORD != '' and PASSWORD != Null:
        if not mpdAuth(client, PASSWORD):
            printStatus('failure', 'failed to auth against MPD server')
            sys.exit(-1)

    command = os.environ['SCRIPT_NAME'].replace('/mpd/status/', '')

    if command == 'currentsong/':
        dumpClientObject(client.currentsong())
    elif command == 'cover/':
        getCoverImage(client)
    else:
        dumpClientObject(client.status())

if __name__ == "__main__":
    main()