from flask import Flask
from flask import jsonify
import base64
from model import model
app = Flask(__name__)

import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<url>')
def hello(url=None):
    base64_bytes = url.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    url = message_bytes.decode('ascii')
    res = model(url)

    return jsonify(res)

if __name__ == '__main__':
    app.run()
