import ConfigParser
from flask import Flask, render_template, request
from database_setup import Category, Item, session
import db
app = Flask(__name__)


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
        category=db.getCategory(category_id), items=db.getItems(category_id))

@app.route('/catalog/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return render_template('delete.j2', thing=db.getCategory(category_id))

@app.route('/catalog/postme', methods=['POST'])
def posttest():
    return 'Got a post, dude.\n' + str(request.json) + '\n'

@app.route('/catalog/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'Edit page for category_id: ' + str(category_id)

@app.route('/catalog/item/<int:item_id>', methods=['GET'])
def viewItem(item_id):
    return render_template('item.j2', item=db.getItem(item_id))

@app.route('/catalog/item/<int:item_id>/edit')
def editItem(item_id):
    return render_template('item-editor.j2',
        item=db.getItem(item_id), categories=db.getCategories())

@app.route('/catalog/item/<int:item_id>/delete')
def confirmItemDelete(item_id):
    item = db.getItem(item_id)
    return render_template('delete.j2', thing=item)

@app.route('/catalog/item/create', methods=['POST'])
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

@app.route('/catalog/item/delete', methods=['POST'])
def deleteItem():
    if request.json is not None:
        data = request.json
        db.deleteItem(data['item_id'])
        return 'Nice!'
    else:
        return 'ERROR!'

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
