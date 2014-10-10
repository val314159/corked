#!/usr/bin/env python

import os,sys,traceback as tb,bottle

# #  Logging stuff  # #
import logging
logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# #  Insert session middleware  # #
def get_session_middleware():
    from beaker.middleware import SessionMiddleware
    session_opts = {
        'session.cookie_expires': True,
        'session.encrypt_key': 'please use a random key and keep it secret!',
        'session.httponly': True,
        'session.timeout': 3600 * 24,  # 1 day
        'session.type': 'cookie',
        'session.validate_key': True,
        }
    return SessionMiddleware(bottle.app(), session_opts)

from cork import Cork
from cork.backends import SQLiteBackend
b = SQLiteBackend(os.environ['DBNAME'])

# not really a monkey patch, more like a kludge.
# just to get auto connect mode.
# ideally the backend driver would do its own transations.
b._connection.isolation_level = None

backend = Cork(backend=b,
               email_sender=os.environ['EMAIL_SENDER'],
               smtp_url=os.environ['SMTP_URL'])

def get_app():
    return get_session_middleware()

