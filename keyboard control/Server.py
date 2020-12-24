PORT = 8000

from http.server import BaseHTTPRequestHandler
import socketserver
import json
from readchar import readkey
from sys import argv

from Time import Time

httpd = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        print("Write to stdin")
        while True:
            key = readkey()
            if key == '\x03':
                self.finish()
                self.server.shutdown()
                break

            data = {"action": key}
            print(Time(), 'Sending', data)
            self.wfile.write(bytes(json.dumps(data), encoding='utf8'))
            self.wfile.write(b'\n')

    def do_POST(self):
        self.send_response(204)
        self.end_headers()
        with open('steveholt-uploaded.jpg', 'wb') as File:
            File.write(self.rfile.read())

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT),
                                Handler,
                                bind_and_activate=False) as httpd:
        httpd.server = httpd
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        print("HTTPServer Serving at port", PORT)
        httpd.serve_forever()