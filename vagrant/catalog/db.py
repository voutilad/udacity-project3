from models import Category, Item
from database import db_session


def getItem(item_id):
    item = db_session.query(Item).filter(Item.id == item_id).one()
    return item

def putItem(item):
    db_session.add(item)
    print 'Creating new item: ' + str(item)
    db_session.commit()

def deleteItem(item_id):
    item = getItem(item_id)
    if item is None:
        print 'Cannot delete non-existant item with id: ' + str(item_id)
    else:
        db_session.delete(item)
        db_session.flush()
        print 'Deleted item ' + str(item)


def getCategory(category_id):
    category = db_session.query(Category).filter(Category.id == category_id).one()
    return category

def getItems(category_id):
    items =  db_session.query(Item).filter(Item.category_id == category_id).all()
    return items

def getCategories():
    categories = db_session.query(Category).all()
    return categories
