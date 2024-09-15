from flask import Flask, request, jsonify
import requests
import ssl
from requests.adapters import HTTPAdapter

app = Flask(__name__)

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

# Define the route for your form submission
@app.route('/api/submit_form', methods=['POST'])
def submit_form():
    content = request.json

    url = 'http://3.111.52.141:5000/api/submit_form'  # The Flask API URL you are hitting
    data = {
        'name': content.get('name', ''),
        'id_number': content.get('id_number', ''),
        'email': content.get('email', '')
    }

    with requests.Session() as session:
        session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_TLSv1_2))
        response = session.post(url, json=data)
    
    if response.status_code == 200:
        result = {"status": "success", "data": response.json()}
    else:
        result = {"status": "error", "message": "Failed to submit data"}

    return jsonify(result)

# if __name__ == '__main__':
    # app.run(debug=True)
