#!/usr/bin/env python

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
        print '{ "status": "failure", "message": "unknown command" }'

if __name__ == "__main__":
    main()