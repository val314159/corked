#!/usr/bin/env python

import os,sys,traceback as tb,bottle

# #  Logging stuff  # #
import logging
logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# #  Insert session middleware  # #
from beaker.middleware import SessionMiddleware
app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)

from pages import *

# #  Web application main  # #
def serve():
    #global b, aaa
    from cork import Cork
    from cork.backends import SQLiteBackend
    b = SQLiteBackend(os.environ['DBNAME'], initialize=False)

    import sqlite3
    b._connection = sqlite3.connect(b._filename)

    aaa = Cork(backend=b,
               email_sender=os.environ['EMAIL_SENDER'],
               smtp_url=os.environ['SMTP_URL'])
    set_aaa(aaa)
    bottle.run(app=app, quiet=False, reloader=True, debug=True)
    pass

if __name__=='__main__': serve()

