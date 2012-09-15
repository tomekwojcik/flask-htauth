# -*- coding: utf-8 -*-

import base64
from flask import Response, g, request

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from functools import wraps

from .htpasswd import check_password, read_htpasswd

__all__ = ['HTAuth', 'authenticated']


class HTAuth(object):
    """
    This class controls basic HTTP authentication integration with Flask apps.

    You can either bind the app to an instance::

        app = Flask(__app__)
        auth = HTAuth(app)

    or create the auth object once and bind it later::

        auth = HTAuth()

        def create_app():
            app = Flask(__name__)
            auth.init_app(app)
            return app
    """

    def __init__(self, app=None):
        self._app = app

        if self._app:
            self.init_app(self._app)

    def init_app(self, app):
        """Bind the **app** to HTAuth instance."""
        app.before_request(self._before_request)

    def _before_request(self):
        ctx = stack.top
        if ctx and not hasattr(ctx, 'htauth'):
            if 'HTAUTH_HTPASSWD_PATH' in ctx.app.config:
                _users = read_htpasswd(ctx.app.config['HTAUTH_HTPASSWD_PATH'])
                _realm = ctx.app.config.get('HTAUTH_REALM', 'Protected Area').\
                    encode('utf-8')

                settings = {
                    'users': _users,
                    'realm': _realm
                }

                ctx.htauth = settings


def _unauthorized_response():
    ctx = stack.top
    if ctx and hasattr(ctx, 'htauth'):
        rsp = Response(
            response='Unauthorized',
            status=401,
            headers={
                'WWW-Authenticate': 'Basic realm="%s"' % ctx.htauth['realm']
            },
            mimetype='text/plain',
            content_type='text/plain;charset=utf-8'
        )

        return rsp

    return None


def authenticated(viewfunc):
    """Decorate **viewfunc** with this decorator to require HTTP auth on the
    view."""
    @wraps(viewfunc)
    def wrapper(*args, **kwargs):
        ctx = stack.top
        if ctx and hasattr(ctx, 'htauth'):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return _unauthorized_response()

            if not auth_header.startswith('Basic '):
                raise RuntimeError('Flask-HTAuth supports only Basic auth.')

            auth_header = auth_header.replace('Basic ', '')
            auth_header = base64.b64decode(auth_header)
            username, password = auth_header.split(':', 1)

            if not username in ctx.htauth['users']:
                return _unauthorized_response()

            if not check_password(password, ctx.htauth['users'][username]):
                return _unauthorized_response()

            g.htauth_user = username

        return viewfunc(*args, **kwargs)

    return wrapper
