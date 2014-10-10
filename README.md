Corky (v0.1)
=========

Corky is an authorization server for cork (bottle/flask)
It can use multiple backends. *(default uses sqlite3)*

You can log in directly to the server, or use it thru HTTP calls.

### Install It

    . install.sh

### Run It

    . env.sh run

After you run it,
 proceed to [The Login Screen](http://localhost:8080/login)

------------
###FAQ

1. Why does this exist?

 - I needed an authorization server, not a library.  I also didn't want a ton of dependencies (KISS).
So I took the simple example program and started adding features that I needed.

------------

### Production Use:

>Ideally, you'd run this just for ONLY http://localhost and then put nginx (or some other industrial grade HTTPS server) in front of this for production use.

Also,
- maybe not run it in debug mode
- or reloader mode
- also use gevent
- put it in the background
- use the logger decently

------------
