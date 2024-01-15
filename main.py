import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import socket
import urllib.parse

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        elif pr_url.path == '/style.css':
            self.send_static_file('style.css')
        elif pr_url.path == '/logo.png':
            self.send_static_file('logo.png')
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static_file(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'text/css' if filename.endswith('.css') else 'image/png')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

def run_http_server():
    server_address = ('', 3000)
    http = HTTPServer(server_address, HttpHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def run_socket_server():
    server_address = ('', 5000)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(server_address)

    while True:
        data, addr = udp_socket.recvfrom(1024)
        message = json.loads(data.decode())

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with open('storage/data.json', 'a') as f:
            json.dump({timestamp: message}, f)
            f.write('\n')

if __name__ == '__main__':
    http_thread = Thread(target=run_http_server)
    socket_thread = Thread(target=run_socket_server)

    http_thread.start()
    socket_thread.start()

    http_thread.join()
    socket_thread.join()
