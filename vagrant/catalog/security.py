'''
Security classes and methods
'''
from functools import wraps

class SecurityCheck(object):
    '''
    Class used for decorating Flask route definitions with logic for checking
    if a requesting user is authenticated and allowed to proceed
    '''
    __name__ = 'SecurityCheck'

    def __init__(self, session=None):
        self.session = session

    def __call__(self, function):

        @wraps(function)
        def decorated_function(*args, **kwargs):
            if self.session is not None and self.session.has_key('credentials'):
                print 'Yup, session here' + str(self.session)
            else:
                print 'No session deets?!'
            return function(*args, **kwargs)

        return decorated_function
