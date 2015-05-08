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
                print "espero"
                self.data = self.rfile.readline().strip()
                print "datos!"
                print "{} wrote:".format(self.client_address[0])
                print self.data
                # Likewise, self.wfile is a file-like object used to write back
                # to the client
                self.wfile.write(self.data.upper())
            finally:
                return

    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        print "Finish"
        self.server.android = None

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

HOST, PORT = "0.0.0.0", 8001
server = None

def getSocketServer():
    global server
    return server

def runServerSocket():
    global server
    if server is None:
        server = AndroidTCPServer((HOST, PORT))
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()