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

from mpdrest.common import Config

class MpdLib:
    @staticmethod
    def mpdConnect(client):
        con_id = {'host': Config.MPD_HOST, 'port': Config.MPD_PORT}

        try:
            client.connect(**con_id)
        except SocketError:
            return False
        return True

    @staticmethod
    def mpdAuth(client, secret):
        try:
            client.password(secret)
        except CommandError:
            return False
        return True

    @staticmethod
    def getImage(current):
        folder = current['file'].rsplit('/', 2)

        path = Config.MUSICPATH

        for part in folder[:len(folder)-1:]:
            path = path + '/' + part

        path = path + '/folder.jpg'

        return file(path, "rb").read()