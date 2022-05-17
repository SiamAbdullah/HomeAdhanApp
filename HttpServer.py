import socket
from urllib.parse import quote
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread

class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, port):
        super().__init__()
        self.daemon = True
        handler = SimpleHTTPRequestHandler
        self.httpd = TCPServer(("", port), handler)

    def run(self):
        """Start the server"""
        print("Start HTTP server")
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        print("Stop HTTP server")
        self.httpd.socket.close()