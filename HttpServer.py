from time import sleep
from urllib.parse import quote
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread

class CustomHttpRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':	'image/svg+xml',
        '.css':	'text/css',
        '.js':'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }

    def do_GET(self):
        try:
            SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            print("Get Request error: " + e)
        return


class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, port):
        super().__init__()
        self.daemon = True
        self.httpd = TCPServer(("", port), CustomHttpRequestHandler)
        self.isAlive=True

    def run(self):
        """Start the server"""
        print("Start HTTP server")
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        print("Stop HTTP server")
        self.httpd.socket.close()
