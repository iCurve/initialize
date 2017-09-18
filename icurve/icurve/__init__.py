# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from flask import Flask
from flask_cors import CORS

from .v1 import bp
from .v1.models import db


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['STATIC_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icurve.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    app.register_blueprint(bp, url_prefix='/v1')
    CORS(app)
    return app


if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=8080)
