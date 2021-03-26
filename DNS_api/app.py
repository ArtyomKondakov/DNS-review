from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import base64
import pandas as pd
from dns_parser import get_all_links
from model import model
import os
from flask import send_from_directory
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=False, nullable=True)
    name = db.Column(db.String(80), unique=False, nullable=True)
    review_class = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        return  self.url

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/<url>')
def hello(url=None):
    base64_bytes = url.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    url = message_bytes.decode('ascii')
    links_pars = json.loads(url)
    links_sql = [str(v) for v in Product.query.order_by(Product.url).all()]
    df = pd.DataFrame()
    res = ''
    for link_pars in links_pars:
        if link_pars in links_sql:
            link = Product.query.filter_by(review_class=link_pars).first()
            p = Product.query.filter_by(url=link_pars).first()
            df = df.append(pd.DataFrame([[p.name, p.review_class, p.url]],
                                                columns=['name', 'review', 'url']), ignore_index=True)
            res = df.to_json()

        else:
            res = model(links_pars)
            for row , col in res.iterrows():
            #                if col['url'] != 'NULL':
                prod = Product(url=col['url'], name = col['name'], review_class=col['review'])
                db.session.add(prod)
                db.session.commit()
            res = res.to_json()  # переводим в json
            break
    return res


if __name__ == '__main__':
    app.run()
