# -*- coding: utf-8 -*-

import codecs
import os
import tempfile
from unittest import TestCase

from flask_htauth.htpasswd import apache_md5crypt, check_password, read_htpasswd

HTPASSWD_ASCII = """md5:$apr1$E0JR/koh$ZX4Gx.XaJ4.uW/u/f71Xr1
sha:{SHA}2PRZAyDhNDqRW2OUFwZQqPNdaSY=
crypt:QtjXmrxfdfid6
"""

HTPASSWD_UTF8 = u"""utf8md5:$apr1$d2KbVD6r$AUAF3s8XEEbpb81Ey0XE.0
utf8sha:{SHA}W6aFBjXnMTMSggQEc6wsmMBufXk=
utf8crypt:.JR7FYLagYAMc
"""


class ParseHtpasswdTestCase(TestCase):
    def setUp(self):
        _, self.htpasswd_ascii_path = tempfile.mkstemp()
        f = open(self.htpasswd_ascii_path, 'w')
        f.write(HTPASSWD_ASCII)
        f.close()

    def tearDown(self):
        os.unlink(self.htpasswd_ascii_path)

    def test_parse_htpasswd(self):
        users = read_htpasswd(self.htpasswd_ascii_path)
        assert len(users) == 3
        assert 'md5' in users
        assert 'sha' in users
        assert 'crypt' in users


class CheckPasswordTestCase(TestCase):
    def setUp(self):
        _, self.htpasswd_ascii_path = tempfile.mkstemp()
        f = open(self.htpasswd_ascii_path, 'w')
        f.write(HTPASSWD_ASCII)
        f.close()

        _, self.htpasswd_utf8_path = tempfile.mkstemp()
        f = codecs.open(self.htpasswd_utf8_path, 'w', 'utf-8')
        f.write(HTPASSWD_UTF8)
        f.close()

        self.users = read_htpasswd(self.htpasswd_ascii_path)
        self.users_utf8 = read_htpasswd(self.htpasswd_utf8_path)

    def tearDown(self):
        os.unlink(self.htpasswd_ascii_path)
        os.unlink(self.htpasswd_utf8_path)

    def test_check_password(self):
        assert check_password('md5', self.users['md5']) == True
        assert check_password('sha', self.users['sha']) == True
        assert check_password('crypt', self.users['crypt']) == True

    def test_check_password_utf8(self):
        assert check_password(u'ęóąśłżźćń', self.users_utf8['utf8md5']) == True
        assert check_password(u'ęóąśłżźćń', self.users_utf8['utf8sha']) == True
        assert check_password(u'ęóąśłżźćń', self.users_utf8['utf8crypt']) == True