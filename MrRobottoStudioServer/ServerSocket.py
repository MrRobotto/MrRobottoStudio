import socketserver
import threading

import MrRobottoStudioServer.utils as utils
import MrRobottoStudioServer.settings as settings


class MyTCPHandler(socketserver.StreamRequestHandler):

    def setup(self):
        socketserver.StreamRequestHandler.setup(self)
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
            socketserver.StreamRequestHandler.finish(self)
        finally:
            return

class AndroidTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self):
        socketserver.TCPServer.__init__(self,(utils.get_ip(), settings.SERVER_SOCKET_PORT), MyTCPHandler)
        self.android = None
        self.server_thread = threading.Thread(target=self.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
    def send_update(self):
        if self.android:
            self.android.sendall("UPDT".encode('ascii'))
    def is_connected(self):
        return self.android != None
    def has_changed(self):
        r = self.changed
        self.changed = False
        return r
