'''
Udacity Fullstack Nanodegree Project 3 - Item Catalog
Author: Dave Voutila
'''
import ConfigParser
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from models import Category, Item, User
from database import DB_SESSION
import db, utils

### security stuff
from flask import session as login_session
from security import SecurityCheck
from werkzeug.utils import secure_filename, escape
import security, os

UPLOAD_PREFIX = './static/'
UPLOAD_FOLDER = 'uploads'

APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@APP.route('/')
@APP.route('/catalog')
def home():
    ''' Main landing page/view for the Catalog App '''
    categories = DB_SESSION.query(Category).all()
    counts = {}
    for category in categories:
        counts.update({category.category_id : db.get_item_count(category.category_id)})
    items = DB_SESSION.query(Item).order_by(Item.modified_date.desc()).limit(20).all()

    return render_template('catalog.j2', categories=categories,
                           items=items, counts=counts,
                           login_session=login_session)

@APP.route('/loginview')
def login_view():
    if login_session is not None and login_session.has_key('credentials'):
        return request.referrer
    return render_template('login.j2', login_session=login_session)

@APP.route('/login')
def login():
    ''' Navigates the OAuth2 protocol, inspecting first for an OAuth2 code.
        If no code, redirects the requestor to the Google signin page to
        generate one. Google redirects the user back once auth'd.
    '''

    if not request.args.has_key('code'):
        state = security.generate_state()
        login_session['state'] = state
        return redirect(security.get_auth_url(state))
    else:
        print request.args.get('state', '')
        print login_session['state']
        if request.args.get('state', '') != login_session['state']:
            print 'Failure to auth user. Mismatch states.'
            flash('Failed to sign in.')
            return redirect(url_for('home'))
        else:
            credentials = security.validate_code(request.args.get('code'))
            login_session['credentials'] = credentials.to_json()
            (access_token, user_id) = security.validate_credentials(credentials)
            user_data = security.get_user_data(access_token)
            if user_data is not None:
                login_session['username'] = user_data['username']
                login_session['picture'] = user_data['picture']
                login_session['email'] = user_data['email']
                login_session['access_token'] = access_token
                login_session['gplus_id'] = user_id
                if db.get_user(login_session['username']) is None:
                    db.register_user(User(user_id=login_session['email'],
                                          name=login_session['username'],
                                          email=login_session['email'],
                                          picture=login_session['picture']))

                flash('Logged in successfully as ' + login_session['username'])
        return redirect(url_for('home'))



@APP.route('/logout')
def logout():
    ''' Generate Logout view '''
    if login_session is None or not login_session.has_key('credentials'):
        #user not logged in
        flash('Huh...no user logged in!')
    else:
        username = login_session['username']
        access_token = login_session['access_token']
        if security.logout_user(username, access_token) == True:
            flash('Logged out as ' + username)
            del login_session['credentials']
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['state']
        else:
            flash('Error logging out as ' + username + '!')
    return redirect(url_for('home'))

### categories

@APP.route('/catalog/<string:category_id>')
def view_category(category_id):
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
@SecurityCheck(session=login_session, login_route='home')
def new_category():
    ''' Overloaded method:
            * GET - Constructs view for creating a new Category
            * POST - REST API call for creating a new Category
    '''
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = utils.slugify(name)
        user = db.get_user(login_session['email'])
        db.put_category(Category(category_id=category_id,
                                 name=name,
                                 description=description,
                                 created_by_id=user.user_id))
        return redirect(url_for('view_category',
                                category_id=category_id,
                                login_session=login_session))
    else:
        return render_template('category-new.j2', login_session=login_session)

@APP.route('/catalog/category/<string:category_id>/delete', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='view_category')
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
@SecurityCheck(session=login_session, login_route='view_category')
def new_item(category_id):
    ''' Constructs view for adding an Item to a Category '''
    if request.method == 'POST':
        if not security.validate_state(login_session,
                                       request.form.get('state', '')):
            flash('Error: invalid state!')
            return redirect(url_for('new_item', category_id=category_id))
        name = request.form['name']
        description = request.form['description']
        item_id = utils.slugify(name)
        user = db.get_user(login_session['email'])
        item = Item(item_id=item_id, category_id=category_id,
                    name=name, description=description,
                    created_by_id=user.user_id)
        db.put_item(item)
        return redirect(url_for('view_category',
                                category_id=category_id,
                                login_session=login_session))
    else:
        category = db.get_category(category_id)
        return render_template('item-new.j2',
                               category_name=category.name,
                               category_id=category_id,
                               login_session=login_session,
                               state=login_session.get('state', ''))

@APP.route('/catalog/<string:category_id>/<string:item_id>')
def view_item(item_id, category_id):
    ''' Constrcts view for item display. '''
    category_name = db.get_category(category_id).name
    item = db.get_item(item_id, category_id)
    creator = db.get_user(item.created_by_id)
    return render_template('item.j2',
                           item=item,
                           creator=creator,
                           login_session=login_session,
                           category_name=category_name)

@APP.route('/catalog/<string:category_id>/<string:item_id>/update', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='view_item')
def update_item(item_id, category_id):
    ''' Constructs view for modifying or updating a given item '''
    if request.method == 'POST':
        if not security.validate_state(login_session,
                                       request.form.get('state', '')):
            flash('Error: invalid state!')
            return redirect(url_for('update_item', item_id=item_id,
                                    category_id=category_id))
        name = request.form['name']
        description = request.form['description']
        new_category_id = request.form['category_id']
        picture = None
        image = request.files['file']
        if image and utils.allowed_file(image.filename):
            filename = secure_filename(item_id)
            picture = os.path.join(APP.config['UPLOAD_FOLDER'], filename)
            image.save(os.path.join(UPLOAD_PREFIX, UPLOAD_FOLDER, filename))
        changes = {'modified_date': 'NOW()'}
        if name:
            changes.update({'name':name})
        if description:
            changes.update({'description':description})
        if new_category_id:
            changes.update({'category_id':new_category_id})
        if picture:
            changes.update({'picture':picture})
        item = Item(item_id=item_id, category_id=category_id)
        db.update_item(item, changes)
        return redirect(url_for('view_item', item_id=item_id,
                                category_id=new_category_id,
                                login_session=login_session))
    else:
        return render_template('item-editor.j2',
                               item=db.get_item(item_id, category_id),
                               item_category=db.get_category(category_id),
                               categories=db.get_categories(),
                               login_session=login_session,
                               state=login_session.get('state', ''))

@APP.route('/catalog/<string:category_id>/<string:item_id>/delete', methods=['GET', 'POST'])
@SecurityCheck(session=login_session, login_route='view_item')
def delete_item(item_id, category_id):
    ''' REST API for deleting an item '''
    if request.method == 'POST':
        db.delete_item(item_id, category_id)
        return redirect(url_for('view_category', category_id=category_id,
                                login_session=login_session))
    else:
        return 'TODO! Sup girl. You want a delete confirmation or something?'

@APP.route('/catalog/item/new', methods=['POST'])
@SecurityCheck(session=login_session, login_route='view_category')
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
