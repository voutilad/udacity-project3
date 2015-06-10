from flask import Flask
from database_setup import Category, Item, session
app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():
    s = session()
    categories = s.query(Category).all()

    output = ''
    for category in categories:
        output += '<div>{cat}</div>'.format(cat=category.name)

    return output

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
