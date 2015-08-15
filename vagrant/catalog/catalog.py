import ConfigParser
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask import session as login_session
import random, string
from models import Category, Item
from database import db_session
import db, utils
app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def home():
    categories = db_session.query(Category).all()
    counts = {}
    for category in categories:
        counts.update({category.id : db.getItemCount(category.id)})
    items = db_session.query(Item).order_by(Item.modified_date.desc()).limit(20).all()

    return render_template('catalog.j2', categories=categories, items=items, counts=counts)

### session handling & login

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.j2', client_id=app.client_id)

### categories

@app.route('/catalog/<string:category_id>')
def showCategory(category_id):
    category = db.getCategory(category_id)
    items = db.getItems(category_id)

    if utils.request_wants_json(request):
        return jsonify(category=category.to_json(),
                       items=[i.to_json() for i in items])
    else:
        return render_template('category.j2', category=category,items=items)

@app.route('/catalog/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = utils.slugify(name)
        db.putCategory(Category(name=name, id=category_id, description=description))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('category-new.j2')

@app.route('/catalog/category/<string:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = db.getCategory(category_id)
    items = db.getItems(category_id)

    if request.method == 'GET':
        if items:
            print '[DEBUG]: category ' + category.id + ' has items. Need confirmation.'
            return render_template('category-delete.j2', category=category, items=items)
        else:
            print '[DEBUG]: category ' + category.id + ' empty. Deleting.'
            db.deleteCategory(category)
            return redirect(url_for('home'))
    else: #POST
        if items:
            db.deleteItems(items)
        db.deleteCategory(category)
        if utils.request_wants_json(request):
            return 'OK' #TODO
        else:
            return redirect(url_for('home'))

@app.route('/catalog/category/<string:category_id>/edit')
def editCategory(category_id):
    return 'Edit page for category_id: ' + str(category_id)

### items

@app.route('/catalog/<string:category_id>/newitem', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_id = utils.slugify(item_name)
        db.putItem(Item(name=item_name, description=item_description,
                   id=item_id, category_id=category_id))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        category = db.getCategory(category_id)
        return render_template('item-new.j2', category_name=category.name,
                               category_id=category_id)

@app.route('/catalog/<string:category_id>/<string:item_id>')
def viewItem(item_id, category_id):
    return render_template('item.j2', item=db.getItem(item_id, category_id))

@app.route('/catalog/<string:category_id>/<string:item_id>/update', methods=['GET', 'POST'])
def updateItem(item_id, category_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        changes = {'modified_date': 'NOW()'}
        if name:
            changes.update({'name':name})
        if description:
            changes.update({'description':description})

        db.updateItem(Item(id=item_id, category_id=category_id), changes)
        return redirect(url_for('viewItem', item_id=item_id, category_id=category_id))
    else:
        return render_template('item-editor.j2',
                               item=db.getItem(item_id, category_id),
                               categories=db.getCategories())

@app.route('/catalog/<string:category_id>/<string:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id, category_id):
    if request.method == 'POST':
        db.deleteItem(item_id, category_id)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return 'TODO! Sup girl. You want a delete confirmation or something?'

@app.route('/catalog/item/new', methods=['POST'])
def createItem():
    if request.json is not None:
        data = request.json
        item = Item(name=data['name'],
                    description=data['description'],
                    category_id=data['category_id'])
        db.putItem(item)

        return 'Nice!'
    else:
        return 'ERROR!'



@app.teardown_appcontext
def shutdown_session(exception):
    db_session.remove()

############################################


if __name__ == '__main__':
    config = ConfigParser.SafeConfigParser(
        {'debug': True, 'host': '0.0.0.0', 'port': 5000})
    config.read('config.cfg')

    app.secret_key = config.get('oauth', 'secret_key')
    app.client_id = config.get('oauth', 'client_id')
    app.debug = config.getboolean('server', 'debug')
    app.run(host=config.get('server', 'host'),
            port=config.getint('server', 'port'))
