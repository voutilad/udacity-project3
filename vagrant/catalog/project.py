import ConfigParser
from flask import Flask, render_template
from database_setup import Category, Item, session
app = Flask(__name__)

def getItem(item_id):
    s = session()
    return s.query(Item).filter(Item.id == item_id).one()

def getCategory(category_id):
    s = session()
    return s.query(Category).filter(Category.id == category_id).one()

def getItems(category_id):
    s = session()
    return s.query(Item).filter(Item.category_id == category_id).all()

def getCategories():
    s = session()
    return s.query(Category).all()

###############################################

@app.route('/')
@app.route('/catalog')
def home():
    s = session()
    categories = s.query(Category).all()
    items = s.query(Item).limit(20).all()

    return render_template('catalog.j2', categories=categories, items=items)

@app.route('/catalog/<int:category_id>')
def showCategory(category_id):
    return render_template('category.j2',
        category=getCategory(category_id), items=getItems(category_id))

@app.route('/catalog/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return render_template('delete.j2', thing=getCategory(category_id))

@app.route('/catalog/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'Edit page for category_id: ' + str(category_id)

@app.route('/catalog/item/<int:item_id>')
def viewItem(item_id):
    return render_template('item.j2', item=getItem(item_id))

@app.route('/catalog/item/<int:item_id>/edit')
def editItem(item_id):
    return render_template('item-editor.j2',
        item=getItem(item_id), categories=getCategories())

@app.route('/catalog/category/new')
def newCategory():
    return render_template('category-new.j2')


############################################


if __name__ == '__main__':
    config = ConfigParser.SafeConfigParser(
        {'debug': True, 'host': '0.0.0.0', 'port': 5000})
    config.read('config.cfg')

    app.debug = config.getboolean('server', 'debug')
    app.run(host = config.get('server', 'host'),
        port=config.getint('server', 'port'))
