from flask import Flask
from flask import render_template
from dns_parser import parser
import base64
from model import model
app = Flask(__name__)





import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
"""@app.route('/')
def hello_world():
    return ''
"""
# http://127.0.0.1:5000/hhasdf9sdahfuisadfhsauifhsad
@app.route('/<url>')
def hello(url=None):
    base64_bytes = url.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    url = message_bytes.decode('ascii')

    #url = url.replace('~', "/")
    return render_template('hello.html', url=url, res=model(url))

if __name__ == '__main__':
    app.run()
