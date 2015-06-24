from models import Category, Item
from database import db_session


def getItem(item_id, category_id):
    item = db_session.query(Item).filter(Item.id == item_id, Item.category_id == category_id).one()
    return item

def putItem(item):
    db_session.add(item)
    print '[db]>> Creating new item: ' + str(item)
    db_session.commit()

def updateItem(item, changes):
    db_session.query(Item) \
              .filter(Item.id == item.id, Item.category_id == item.category_id)\
              .update(changes, synchronize_session=False)
    print '[db]>> Updating item: ' + str(item.id) + ' with changes: ' + str(changes)
    db_session.commit()

def deleteItem(item_id, category_id):
    item = getItem(item_id, category_id)
    if item is None:
        print '[db]>> Cannot delete non-existant item with id: ' + str(category_id) + '/' + str(item_id)
    else:
        db_session.delete(item)
        db_session.commit()
        print '[db]>> Deleted item ' + str(item)

def putCategory(category):
    db_session.add(category)
    print '[db]>> Creating category: ' + str(category)
    db_session.commit()

def getCategory(category_id):
    category = db_session.query(Category).filter(Category.id == category_id).one()
    return category

def getItems(category_id):
    items =  db_session.query(Item).filter(Item.category_id == category_id).all()
    return items

def getCategories():
    categories = db_session.query(Category).all()
    return categories
