Flask-HTAuth
============

.. module:: Flask-HTAuth

**Flask-HTAuth** provides Flask apps with easy to integrate basic HTTP authentication. The extension supports standard htpasswd files.

Source code and issue tracker are available at `GitHub`_.

Installation
------------

Install with the usual:

.. code-block:: none

    pip install flask-htauth

or download source from GitHub:

.. code-block:: none

    git clone https://github.com/tomekwojcik/flask-htauth.git
    cd flask-htauth
    python setup.py develop

Configuration
-------------

Flask-HTAuth uses the following settings:

* ``HTAUTH_HTPASSWD_PATH`` - path to htpasswd file,
* ``HTAUTH_REALM`` - authentication realm (defaults to ``Protected Area``)


Example app
-----------

.. code-block:: python

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

If the request is missing ``Authorization`` header or auth data is invalid the ``authenticated`` decorator will return response that will force the user agent to request authentication data from the user.

Features
--------

* Basic auth,
* Support for MD5, SHA and crypt htpasswd password encrypting.

License
-------

Flask-HTAuth is licensed under MIT License. See `LICENSE`_ for more details.

API
---

.. module:: flask.ext.htauth

.. autoclass:: HTAuth
   :members:

.. autofunction:: authenticated

Credits
-------

Flask-HTAuth is developed by `BTHLabs`_. The extension was inspired by `django-htauth`_. Uses MD5 crypt code from `this snippet`_.

.. _GitHub: http://github.com/tomekwojcik/flask-htauth
.. _LICENSE: http://github.com/tomekwojcik/flask-htauth/blob/master/LICENSE
.. _BTHLabs: http://www.bthlabs.pl/
.. _django-htauth: http://pypi.python.org/pypi/django-htauth/
.. _this snippet: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/325204
