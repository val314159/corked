#!/usr/bin/env python
#
# Copyright (C) 2014 Joel Ward and others, see AUTHORS file.
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under GPLv3+ license, see LICENSE.txt
#
# Orignally forked from Cork example web application

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


# #  Bottle methods  # #

def postd():
    """get POST dict"""
    return bottle.request.params


def post_get(name, default=''):
    """get a HTTP param (get or post)"""
    return bottle.request.params.get(name, default).strip()


@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    x = aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@bottle.route('/auth/login', method=['GET','POST'])
def auth_login():
    """Authenticate users (JSON)"""
    username = post_get('username')
    password = post_get('password')
    try:
        if aaa.login(username, password):
            return dict()
    except:
        pass
    return dict(success=False, errmsg='Access Denied')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    """is user anonymous?"""
    return 'true' if aaa.user_is_anonymous else 'false'

@bottle.route('/logout')
def logout():
    """Log out"""
    aaa.logout(success_redirect='/login')

@bottle.route('/auth/logout',method=['GET','POST'])
def auth_logout():
    """Log out (JSON)"""
    aaa.logout()


@bottle.post('/register')
def register():
    """Send out registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    return 'Please check your mailbox.'

@bottle.route('/auth/register',method=['GET','POST'])
def auth_register():
    """Send out registration email (JSON)"""
    try:
        aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    except:
        return dict(success=False,errmsg='Registration Failed',
                    language='python',trace=tb.format_exc().split('\n'))
    return dict()


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address'))
    return 'Please check your mailbox.'


@bottle.route('/change_password/:reset_code')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.route('/')
def index():
    """Only authenticated users can see this"""
    aaa.require(fail_redirect='/login')
    return 'Welcome! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'


@bottle.route('/auth_require',method=['GET','POST'])
def auth_require():
    """Only authenticated users can see this"""
    try:
        if aaa.require():
            return dict()
    except:
        pass
    return dict(success=False, errmsg='Access Denied')


@bottle.route('/restricted_download')
def restricted_download():
    """Only authenticated users can download this file"""
    aaa.require(fail_redirect='/login')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print "Session from simple_webapp", repr(session)
    aaa.require(fail_redirect='/login')
    return aaa.current_user.role


# Admin-only pages

@bottle.route('/admin')
@bottle.view('admin_page')
def admin():
    """Only admin users can see this"""
    aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles())


@bottle.post('/create_user')
def create_user():
    """Create user"""
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
def delete_user():
    """Delete user"""
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
def create_role():
    """Create role"""
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
def delete_role():
    """Delete role"""
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


# #  Web application main  # #
def serve():
    global b
    global aaa
    from cork import Cork
    from cork.backends import SQLiteBackend
    b = SQLiteBackend(os.environ['DBNAME'], initialize=False)
    aaa = Cork(backend=b,
               email_sender=os.environ['EMAIL_SENDER'],
               smtp_url=os.environ['SMTP_URL'])
    bottle.run(app=app, quiet=False, reloader=True, debug=True)

if __name__ == "__main__": serve()
