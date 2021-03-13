""" Use this module to start an HTTP Server. """

import logging
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer


def start(host: str = "", port: int = 80):
    SERVER_ADDRESS = (host, port)
    server = HTTPServer(SERVER_ADDRESS, Server)
    try:
        logging.debug("Server running on port %i.", port)
        server.serve_forever()
    except KeyboardInterrupt:
        logging.debug("Server closed.")
        server.server_close()


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        # params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
