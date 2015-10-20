'''
Security classes and methods
'''
from functools import wraps
from flask import redirect, url_for, flash

class SecurityCheck(object):
    '''
    Class used for decorating Flask route definitions with logic for checking
    if a requesting user is authenticated and allowed to proceed
    '''
    __name__ = 'SecurityCheck'

    def __init__(self, session=None, login_route=None):
        self.session = session
        self.login_route = login_route

    def __call__(self, function):

        @wraps(function)
        def decorated_function(*args, **kwargs):
            ''' Decorator wrapper function '''
            if self.session is not None and self.session.has_key('credentials'):
                return function(*args, **kwargs)
            else:
                flash('Please login to perform that action.')
                return redirect(url_for(self.login_route))

        return decorated_function
