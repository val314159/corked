'''
small util lib for cors handling (in bottle)
'''
def add_headers(response):
    '''
    call this to slap the proper CORS headers into any dict-like object
    '''
    #allow_methods = ', '.join(['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    allow_methods = ', '.join(['GET', 'HEAD', 'POST', 'OPTIONS'])
    allow_headers = ', '.join(['Origin', 'X-Requested-With', 'Content-Type',
                               'Accept', 'Authorization', 'Access-Token'])
    response.headers['Access-Control-Allow-Credentials'] = 'true';
    #response.headers['Access-Control-Allow-Origin']='http://url:8080'
    response.headers['Access-Control-Allow-Origin'     ] = '*'
    response.headers['Access-Control-Allow-Methods'    ] = allow_methods
    response.headers['Access-Control-Allow-Headers'    ] = allow_headers
    return ['OK']
