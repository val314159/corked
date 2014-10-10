#!/usr/bin/env python

# #  Web application main  # #
def main():
    import gevent.monkey; gevent.monkey.patch_all() 
    import pages, bottle
    from app import get_app
    bottle.run(app=get_app(), reloader=True, debug=True, server='gevent')
    pass

if __name__=='__main__': main()
