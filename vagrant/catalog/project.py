from flask import Flask, render_template
from database_setup import Category, Item, session
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    s = session()
    categories = s.query(Category).all()

    return render_template('main.j2', categories=categories)

@app.route('/category/<int:category_id>')
def showCategory(category_id):
    s = session()
    category = s.query(Category).filter(Category.id == category_id).one()
    items = s.query(Item).filter(Item.category_id == category.id).all()

    return render_template('category.j2', category=category, items=items)

@app.route('/category/<int:category_id>/create')
def newCategory(category_id):
    return 'New category page with id: ' + str(category_id)

@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return 'Delete page for category id: ' + str(category_id)

@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'Edit page for category_id: ' + str(category_id)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
