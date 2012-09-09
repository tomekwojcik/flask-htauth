# -*- coding: utf-8 -*-

import base64
import os
import tempfile
from unittest import TestCase

from test_apps import htauth_app

HTPASSWD = 'test_user:$apr1$/W2gsTdJ$J5A3/jiOC/hph1Gcb.0yN/'


class HTAuthAppTestCase(TestCase):
    def setUp(self):
        _, self.htpasswd_path = tempfile.mkstemp()
        f = open(self.htpasswd_path, 'w')
        f.write(HTPASSWD)
        f.close()

        self.actual_app = htauth_app.create_app(
            HTAUTH_HTPASSWD_PATH=self.htpasswd_path,
            HTAUTH_REALM='Test Realm'
        )
        self.app = self.actual_app.test_client()

    def tearDown(self):
        os.unlink(self.htpasswd_path)

    def test_no_auth(self):
        rsp = self.app.get('/')
        assert rsp.status_code == 200
        assert rsp.data == 'Hello, World!'

    def test_auth_not_ok(self):
        rsp = self.app.get('/secret')
        assert rsp.status_code == 401
        assert rsp.data == 'Unauthorized'
        assert rsp.headers['WWW-Authenticate'] == 'Basic realm="Test Realm"'

        headers = {
            'Authorization': 'Basic %s' % base64.b64encode('spam:eggs')
        }

        rsp = self.app.get('/secret', headers=headers)
        assert rsp.status_code == 401
        assert rsp.data == 'Unauthorized'

        headers = {
            'Authorization': 'Digest meh'
        }

        try:
            rsp = self.app.get('/secret', headers=headers)
        except RuntimeError:
            pass

    def test_auth_ok(self):
        headers = {
            'Authorization': 'Basic %s' % base64.b64encode('test_user:test_password')
        }

        rsp = self.app.get('/secret', headers=headers)
        assert rsp.status_code == 200
        assert rsp.data == 'Hello, test_user!'
