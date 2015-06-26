from models import Category, Item
from database import db_session
from sqlalchemy.exc import IntegrityError


def getItem(item_id, category_id):
    item = db_session.query(Item).filter(Item.id == item_id, Item.category_id == category_id).one()
    return item

def putItem(item):
    try:
        db_session.add(item)
        print '[db]>> Creating new item: ' + str(item)
        db_session.commit()
        return True
    except IntegrityError as e:
        print '[db]>> ERROR: ' + str(e)
        db_session.rollback()
        return False

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
        return False
    else:
        db_session.delete(item)
        db_session.commit()
        print '[db]>> Deleted item ' + str(item)
        return True

def deleteItems(items):
    for item in items:
        db_session.delete(item)
        print '[db]>> Deleting item ' + str(item)
    db_session.commit()

def putCategory(category):
    try:
        db_session.add(category)
        print '[db]>> Creating category: ' + str(category)
        db_session.commit()
        return True
    except IntegrityError as e:
        print '[db]>> Error creating category: ' + str(e)
        db_session.rollback()
        return False

def deleteCategory(category):
    db_session.delete(category)
    db_session.commit()
    print '[db]>> Deleted category ' + str(category)

def getCategory(category_id):
    category = db_session.query(Category).filter(Category.id == category_id).one()
    return category

def getItems(category_id):
    items = db_session.query(Item).filter(Item.category_id == category_id).all()
    return items

def getItemCount(category_id):
    return db_session.query(Item).filter(Item.category_id == category_id).count()

def getCategories():
    categories = db_session.query(Category).all()
    return categories
