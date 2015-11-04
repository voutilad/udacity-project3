'''
Security classes and methods
'''
from functools import wraps
from flask import redirect, url_for, flash
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
import httplib2, json, requests
import hashlib, os

FLOW = flow_from_clientsecrets('client_secrets.json',
                               scope='openid email',
                               redirect_uri='http://localhost:5000/login')

# pylint: disable=R0903
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
                return redirect(url_for(self.login_route, *args, **kwargs))

        return decorated_function

def logout_user(username, access_token):
    ''' Revoke active credentials for a given user, causing them to
        sign in in the future '''

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        print 'Logged out user ' + username
        return True
    else:
        print 'Error logging out user ' + username
        print str(result)

    return False

def generate_state():
    ''' Generate a OAuth2 state token '''
    return hashlib.sha256(os.urandom(1024)).hexdigest()

def validate_state(session, state):
    ''' Simple sanity check if the given state matches the stored state for
        the user's session.
    '''
    server_state = session.get('state')
    if state is None or server_state is None:
        return False
    return server_state == state

def get_auth_url(state):
    ''' Return the URL to Google's OAuth2 service. '''
    url = FLOW.step1_get_authorize_url() + '&state=' + str(state)
    url += '&consent=true'
    return url

def validate_code(code):
    ''' Validates an OAuth2 code and return Credentials if valid. '''
    credentials = FLOW.step2_exchange(code)
    return credentials

def validate_credentials(credentials):
    ''' Validate response credentials from OAUth2 service

        Returns:
            (access_token, user_id) if valid
            None if invalid
    '''
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    if result.get('error') is not None:
        print 'Error validating credentials: ' + str(result.get('error'))
        return None

    user_id = credentials.id_token['sub']

    return (access_token, user_id)

def get_user_data(access_token):
    ''' Looks up user's Google account data, returning a dict of details. '''
    details = {}

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    if data is not None:
        details['username'] = data['name']
        details['picture'] = data['picture']
        details['email'] = data['email']
    else:
        print 'Error looking up user data from Google'
        return None

    return details

def check_expired(credentials_json):
    ''' Reconstruct and check expiration of Credentials '''
    credentials = OAuth2Credentials.from_json(credentials_json)
    return credentials.access_token_expired
