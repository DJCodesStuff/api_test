from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import requests
import ssl
from requests.adapters import HTTPAdapter

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Needed for flash messages to work

class SSLAdapter(HTTPAdapter):
    """Custom HTTPAdapter for specifying SSL version."""
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.create_ssl_context()
        super().init_poolmanager(*args, **kwargs)

    def create_ssl_context(self):
        """Create and return an SSL context with a specified SSL version."""
        return ssl.SSLContext(self.ssl_version)

@app.route('/', methods=['GET'])
def home():
    """Serve the main form page."""
    return render_template('form.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    """Handle data submission and send it to a specified API."""
    data = {
        'name': request.form['name'],
        'id_number': request.form['id_number'],
        'email': request.form['email']
    }
    url = 'http://3.111.52.141:5000/api/submit_form'  # Replace with your actual API endpoint
    with requests.Session() as session:
        session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_TLSv1_2))
        response = session.post(url, json=data)
        
        if response.status_code == 200:
            flash("Data received and processed successfully.", "success")
        else:
            flash("Failed to process data.", "error")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
