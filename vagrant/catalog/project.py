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

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
