# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from flask import Flask

from .v1 import bp
from .v1.models import db

app = Flask(__name__, static_folder='static')
app.config['STATIC_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icurve.db')
db.init_app(app)
with app.test_request_context():
    db.create_all()
app.register_blueprint(
    bp,
    url_prefix='/v1')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
