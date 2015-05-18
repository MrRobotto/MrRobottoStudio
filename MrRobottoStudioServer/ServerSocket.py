import SocketServer
import threading

import utils
import settings


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.server.android = self.request

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        while True:
            try:
                self.data = self.rfile.readline().strip()
                # Likewise, self.wfile is a file-like object used to write back
                # to the client
                self.wfile.write(self.data.upper())
            except:
                return
            finally:
                return

    def finish(self):
        try:
            self.server.android = None
            SocketServer.StreamRequestHandler.finish(self)
        finally:
            return

class AndroidTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self):
        SocketServer.TCPServer.__init__(self,(utils.get_ip(), settings.SERVER_SOCKET_PORT), MyTCPHandler)
        self.android = None
        self.server_thread = threading.Thread(target=self.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
    def send_update(self):
        if self.android:
            self.android.sendall("UPDT")
    def is_connected(self):
        return self.android != None
    def has_changed(self):
        r = self.changed
        self.changed = False
        return r
