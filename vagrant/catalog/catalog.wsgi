#!/usr/bin/python
import sys
sys.path.insert(0, '/var/www/catalog')

from catalog import APP
import pprint

class LoggingMiddleware:

    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):
        errors = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errors)

        def _start_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errors)
            return start_response(status, headers, *args)

        return self.__application(environ, _start_response)

APP.secret_key = 'dWoB5zTwojK7DNWHuW_jPviS'
APP.client_id = '896029245869-6fe6tlho709oukgb2pu651q2sdt8udg5.apps.googleusercontent.com'
application = LoggingMiddleware(APP)
