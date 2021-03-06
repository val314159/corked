import os,sys,traceback as tb,bottle

from app import backend

# #  Bottle methods  # #

def paramd():
    """get HTTP param dict"""
    return bottle.request.params

def param_get(name, default=''):
    """get a HTTP param (get or post)"""
    return bottle.request.params.get(name, default).strip()

def mk_uuid():
    import uuid,json
    id   = str(uuid.uuid1())
    key0 = str(uuid.uuid1())
    key1 = str(uuid.uuid4())
    return json.dumps(dict(id=id,key0=key0,key1=key1))


# #  Pages  # #

from cors import add_headers

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = param_get('username')
    password = param_get('password')
    if backend.login(username, password,
                     success_redirect='/', fail_redirect='/login'):
        print "IDENT VERIFIED"
    else:
        print "IDENT UNVERIFIED"

@bottle.route('/auth/login', method=['HEAD','GET','POST','OPTIONS'])
def auth_login():
    """Authenticate users (JSON)"""
    add_headers(bottle.response)
    if bottle.request.method in ['HEAD','OPTIONS']:
        return []
    username = param_get('username')
    password = param_get('password')
    try:
        if backend.login(username, password):
            print "IDENT VERIFIED"
            return dict(desc=backend.current_user.description)
    except:
        pass
    print "IDENT UNVERIFIED"
    return dict(success=False, errmsg='Access Denied')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    """is user anonymous?"""
    return 'true' if backend.user_is_anonymous else 'false'

@bottle.route('/logout')
def logout():
    """Log out"""
    backend.logout(success_redirect='/login')

@bottle.route('/auth/logout',method=['HEAD','GET','POST','OPTIONS'])
def auth_logout():
    """Log out (JSON)"""
    add_headers(bottle.response)
    if bottle.request.method in ['HEAD','OPTIONS']:
        return []
    backend.logout()

@bottle.post('/register')
def register():
    """Send out registration email"""
    desc=mk_uuid()
    backend.register(param_get('username'), param_get('password'),
                 param_get('email_address'), description=desc)
    return 'Please check your mailbox.'

@bottle.route('/auth/register',method=['HEAD','GET','POST','OPTIONS'])
def auth_register():
    """Send out registration email (JSON)"""
    add_headers(bottle.response)
    if bottle.request.method in ['HEAD','OPTIONS']:
        return []
    try:
        desc=mk_uuid()
        backend.register(param_get('username'), param_get('password'),
                     param_get('email_address'), description=desc)
    except:
        return dict(success=False,errmsg='Registration Failed',
                    language='python',trace=tb.format_exc().split('\n'))
    return dict()


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    backend.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    backend.send_password_reset_email(
        username=param_get('username'),
        email_addr=param_get('email_address'))
    return 'Please check your mailbox.'

@bottle.route('/auth/reset_password',method=['HEAD','GET','POST','OPTIONS'])
def auth_send_password_reset_email():
    """Send out password reset email (JSON)"""
    add_headers(bottle.response)
    if bottle.request.method in ['HEAD','OPTIONS']:
        return []
    backend.send_password_reset_email(
        username=param_get('username'),
        email_addr=param_get('email_address'))
    return dict()


@bottle.route('/change_password/:reset_code')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    backend.reset_password(param_get('reset_code'), param_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.route('/')
def index():
    """Only authenticated users can see this"""
    backend.require(fail_redirect='/login')
    return 'Welcome! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'


@bottle.route('/auth/require',method=['HEAD','GET','POST','OPTIONS'])
def auth_require():
    """Only authenticated users can see this"""
    add_headers(bottle.response)
    if bottle.request.method in ['HEAD','OPTIONS']:
        return []
    try:
        if backend.require():
            return dict()
    except:
        pass
    return dict(success=False, errmsg='Access Denied')


@bottle.route('/restricted_download')
def restricted_download():
    """Only authenticated users can download this file"""
    backend.require(fail_redirect='/login')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print "Session from simple_webapp", repr(session)
    backend.require(fail_redirect='/login')
    return backend.current_user.role


# Admin-only pages

@bottle.route('/admin')
@bottle.view('admin_page')
def admin():
    """Only admin users can see this"""
    backend.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=backend.current_user,
        users=backend.list_users(),
        roles=backend.list_roles())


@bottle.post('/create_user')
def create_user():
    """Create user"""
    try:
        backend.create_user(paramd().username, paramd().role, paramd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
def delete_user():
    """Delete user"""
    try:
        backend.delete_user(param_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
def create_role():
    """Create role"""
    try:
        backend.create_role(param_get('role'), param_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
def delete_role():
    """Delete role"""
    try:
        backend.delete_role(param_get('role'))
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
