import ConfigParser
from flask import Flask, render_template
from database_setup import Category, Item, session
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def index():
    s = session()
    categories = s.query(Category).all()
    items = s.query(Item).limit(20).all()

    return render_template('catalog.j2', categories=categories, items=items)

@app.route('/catalog/<int:category_id>')
def showCategory(category_id):
    s = session()
    category = s.query(Category).filter(Category.id == category_id).one()
    items = s.query(Item).filter(Item.category_id == category.id).all()

    return render_template('category.j2', category=category, items=items)

@app.route('/catalog/category/<int:category_id>/create')
def newCategory(category_id):
    return 'New category page with id: ' + str(category_id)

@app.route('/catalog/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return 'Delete page for category id: ' + str(category_id)

@app.route('/catalog/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'Edit page for category_id: ' + str(category_id)

@app.route('/catalog/item/<int:item_id>')
def viewItem(item_id):
    s = session()
    item = s.query(Item).filter(Item.id == item_id).one()
    return render_template('item.j2', item=item)

@app.route('/catalog/item/<int:item_id>/edit')
def editItem(item_id):
    return 'Edit page for item with id: ' + str(item_id)

if __name__ == '__main__':
    config = ConfigParser.SafeConfigParser(
        {'debug': True, 'host': '0.0.0.0', 'port': 5000})
    config.read('config.cfg')

    app.debug = config.getboolean('server', 'debug')
    app.run(host = config.get('server', 'host'),
        port=config.getint('server', 'port'))
