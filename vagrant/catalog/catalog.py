'''
Udacity Fullstack Nanodegree Project 3 - Item Catalog
Author: Dave Voutila
'''
import ConfigParser
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
import random, string
from models import Category, Item
from database import DB_SESSION
from security import SecurityCheck
import db, utils

### security stuff
from flask import session as login_session, make_response
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, json, requests

APP = Flask(__name__)


@APP.route('/')
@APP.route('/catalog')
def home():
    categories = DB_SESSION.query(Category).all()
    counts = {}
    for category in categories:
        counts.update({category.category_id : db.get_item_count(category.category_id)})
    items = DB_SESSION.query(Item).order_by(Item.modified_date.desc()).limit(20).all()

    return render_template('catalog.j2', categories=categories,
                           items=items, counts=counts,
                           login_session=login_session)

### session handling & login

@APP.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.j2',
                           client_id=APP.client_id, state=state,
                           login_session=login_session)

@APP.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        msg = 'Failed to upgrade the authorization code.'
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error'), 501))
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        msg = "Token's user ID doesn't match."
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != APP.client_id:
        msg = "Token's client ID doesn't match applications"
        response = make_response(json.dumps(msg), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        msg = 'Current user is already connected'
        response = make_response(json.dumps(msg), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Creep on the user
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print 'User logged in as %s' % login_session['username']
    return output

@APP.route('/logout')
def show_logout():
    if login_session is None or not login_session.has_key('credentials'):
        #user not logged in
        return redirect(url_for('home'))

    return render_template('logout.j2')

@APP.route('/gdisconnect')
def gdisconnect():
    if login_session is None or not login_session.has_key('credentials'):
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    credentials = login_session['credentials']
    username = login_session['username']

    #access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        flash('Succesfully logged out ' + username)
        return redirect(url_for('home'))
    else:
        flash('Failed to logout and disconnect session.')
        return redirect(url_for('home'))


### categories

@APP.route('/catalog/<string:category_id>')
def show_category(category_id):
    ''' Overloaded method:
            * accepts: json - returns JSON object response
            * accepts: html - returns view for Category display
    '''
    category = db.get_category(category_id)
    items = db.get_items(category_id)

    if utils.request_wants_json(request):
        return jsonify(category=category.to_json(),
                       items=[i.to_json() for i in items])
    else:
        return render_template('category.j2',
                               category=category,
                               items=items,
                               login_session=login_session)

@APP.route('/catalog/category/new', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def new_category():
    ''' Overloaded method:
            * GET - Constructs view for creating a new Category
            * POST - REST API call for creating a new Category
    '''
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = utils.slugify(name)
        db.put_category(Category(category_id=category_id,
                                 name=name,
                                 description=description))
        return redirect(url_for('show_category',
                                category_id=category_id,
                                login_session=login_session))
    else:
        return render_template('category-new.j2', login_session=login_session)

@APP.route('/catalog/category/<string:category_id>/delete', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def delete_category(category_id):
    ''' Overloaded method:
            * GET - Constructs view for deleting a Category
            * POST - REST API call for deleting a Category
    '''
    category = db.get_category(category_id)
    items = db.get_items(category_id)

    if request.method == 'GET':
        if items:
            print '[DEBUG]: category ' + category.category_id + ' has items. Need confirmation.'
            return render_template('category-delete.j2',
                                   category=category,
                                   items=items,
                                   login_session=login_session)
        else:
            print '[DEBUG]: category ' + category.category_id + ' empty. Deleting.'
            db.delete_category(category)
            return redirect(url_for('home', login_session=login_session))
    else: #POST
        if items:
            db.delete_items(items)
        db.delete_category(category)
        if utils.request_wants_json(request):
            return 'OK' #TODO
        else:
            return redirect(url_for('home', login_session=login_session))

@APP.route('/catalog/category/<string:category_id>/edit')
def edit_category(category_id):
    ''' Constructs view for editing an existing Category '''
    return 'Edit page for category_id: ' + str(category_id)

### items

@APP.route('/catalog/<string:category_id>/newitem', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def new_item(category_id):
    ''' Constructs view for adding an Item to a Category '''
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        item_id = utils.slugify(name)
        item = Item(item_id=item_id, category_id=category_id,
                    name=name, description=description)
        db.put_item(item)
        return redirect(url_for('show_category',
                                category_id=category_id,
                                login_session=login_session))
    else:
        category = db.get_category(category_id)
        return render_template('item-new.j2',
                               category_name=category.name,
                               category_id=category_id,
                               login_session=login_session)

@APP.route('/catalog/<string:category_id>/<string:item_id>')
def view_item(item_id, category_id):
    ''' Constrcts view for item display. '''
    return render_template('item.j2', item=db.get_item(item_id, category_id),
                           login_session=login_session)

@APP.route('/catalog/<string:category_id>/<string:item_id>/update', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def update_item(item_id, category_id):
    ''' Constructs view for modifying or updating a given item '''
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        changes = {'modified_date': 'NOW()'}
        if name:
            changes.update({'name':name})
        if description:
            changes.update({'description':description})
        item = Item(item_id=item_id, category_id=category_id)
        db.update_item(item, changes)
        return redirect(url_for('view_item', item_id=item_id,
                                category_id=category_id,
                                login_session=login_session))
    else:
        return render_template('item-editor.j2',
                               item=db.get_item(item_id, category_id),
                               categories=db.get_categories(),
                               login_session=login_session)

@APP.route('/catalog/<string:category_id>/<string:item_id>/delete', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def delete_item(item_id, category_id):
    ''' REST API for deleting an item '''
    if request.method == 'POST':
        db.delete_item(item_id, category_id)
        return redirect(url_for('show_category', category_id=category_id,
                                login_session=login_session))
    else:
        return 'TODO! Sup girl. You want a delete confirmation or something?'

@APP.route('/catalog/item/new', methods=['POST'])
@SecurityCheck(session=login_session, login_route='show_login')
def create_item():
    ''' REST API for creating new catalog item via POST '''
    if request.json is not None:
        data = request.json
        item = Item(name=data['name'],
                    description=data['description'],
                    category_id=data['category_id'])
        db.put_item(item)

        return 'Nice!'
    else:
        return 'ERROR!'



@APP.teardown_appcontext
def shutdown_session():
    ''' Cleanup database session. '''
    DB_SESSION.remove()

############################################


if __name__ == '__main__':
    CONFIG = ConfigParser.SafeConfigParser(
        {'debug': True, 'host': '0.0.0.0', 'port': 5000})
    CONFIG.read('config.cfg')

    APP.secret_key = CONFIG.get('oauth', 'secret_key')
    APP.client_id = CONFIG.get('oauth', 'client_id')
    APP.debug = CONFIG.getboolean('server', 'debug')
    APP.run(host=CONFIG.get('server', 'host'),
            port=CONFIG.getint('server', 'port'))
