from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import ssl
from requests import Session
from requests.adapters import HTTPAdapter

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.create_ssl_context()
        return super().init_poolmanager(*args, **kwargs)

    def create_ssl_context(self):
        context = ssl.SSLContext(self.ssl_version)
        return context

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        field_data = self.rfile.read(length)
        data = json.loads(field_data)

        with Session() as session:
            session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_TLSv1_2))
            response = session.post('http://your-api-url', json=data)
            result = response.json()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

