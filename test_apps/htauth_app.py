# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_htauth import HTAuth, authenticated

def create_app(**config):
    app = Flask(__name__)
    app.config.update(config)
    app.config['TESTING'] = True

    htauth = HTAuth(app)

    @app.route('/')
    def app_index():
        return 'Hello, World!'

    @app.route('/secret')
    @authenticated
    def app_secret():
        return 'Hello, ' + g.htauth_user + '!'

    return app