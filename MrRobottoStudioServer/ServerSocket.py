import SocketServer
from django.apps import AppConfig
import threading

class ServerSocketConfig(AppConfig):
    name = 'MrRobottoStudioServer'
    verbose_name = "ServerSocket"
    def ready(self):
        AppConfig.ready(self)


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

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address):
        SocketServer.TCPServer.__init__(self,server_address, MyTCPHandler)
        self.android = None

HOST, PORT = "0.0.0.0", 8001
server = None

def getSocketServer():
    global server
    return server

def runServerSocket():
    global server
    if server is None:
        server = ThreadedTCPServer((HOST, PORT))
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()