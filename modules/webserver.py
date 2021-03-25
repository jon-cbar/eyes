""" Use this module to start an HTTP Web Server. """

import logging
import socketserver
import os
from http.server import SimpleHTTPRequestHandler


def startServer(hostName: str = "localhost",
                port: int = 80,
                publicDirectory: str = "public"):
    logging.debug("Starting a web server...")

    logging.debug("Defining the origin directory to start the server.")
    modulesPath = os.path.dirname(__file__)
    publicPath = os.path.join(modulesPath, "..", publicDirectory)
    os.chdir(publicPath)

    address = (hostName, port)
    with socketserver.TCPServer(address, WebHandler) as webServer:
        logging.debug("Web server running on port %i.", port)
        webServer.serve_forever()


class WebHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/'):
            self.path = 'index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
