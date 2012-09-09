# -*- coding: utf-8 -*-

from flask import Flask, g
from flask.ext import htauth
import os

HTPASSWD = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'htpasswd')

app = Flask(__name__)
app.config['HTAUTH_HTPASSWD_PATH'] = HTPASSWD
app.config['HTAUTH_REALM'] = 'Top Secret Area'

auth = htauth.HTAuth(app)

@app.route('/')
def app_index():
    return 'Hello, World!'

@app.route('/secret')
@htauth.authenticated
def app_secret():
    return 'Hello, ' + g.htauth_user + '!'

if __name__ == '__main__':
    app.debug = True
    app.run()
