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