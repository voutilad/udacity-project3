''' Database methods for CRUD '''
from models import Category, Item, User
from database import DB_SESSION
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

def register_user(user):
    ''' Record a user or update the last login datetime '''
    try:
        DB_SESSION.add(user)
        print '[db]>> Registered previously unknown user: ' + str(user.user_id)
        DB_SESSION.commit()
        return True
    except IntegrityError as error:
        print '[db]>> ERROR:' + str(error)
        DB_SESSION.rollback()
        return False

def get_user(user_id):
    ''' Look up a User by their unique id (often email) '''
    try:
        user = DB_SESSION.query(User).filter(User.user_id == user_id).one()
    except NoResultFound:
        print '[db]>> Could not look up user with user_id: ' + str(user_id)
        return None
    return user

def get_item(item_id, category_id):
    ''' Retrieve an item by item_id and category_id from the database. '''
    try:
        item = DB_SESSION.query(Item).filter(Item.item_id == item_id,
                                             Item.category_id == category_id).one()
    except NoResultFound:
        msg = '[db]>> No item found for item_id: ' + str(item_id)
        print msg + ', category_id: ' + str(category_id)
        return None
    return item

def put_item(item):
    ''' Put an item into the database, overwriting any existing with same id. '''
    try:
        DB_SESSION.add(item)
        print '[db]>> Creating new item: ' + str(item)
        DB_SESSION.commit()
        return True
    except IntegrityError as error:
        print '[db]>> ERROR: ' + str(error)
        DB_SESSION.rollback()
        return False

def update_item(item, changes):
    ''' Update an item in the database with given changes. '''
    DB_SESSION.query(Item) \
              .filter(Item.item_id == item.item_id, Item.category_id == item.category_id)\
              .update(changes, synchronize_session=False)
    print '[db]>> Updating item: ' + str(item.item_id) + ' with changes: ' + str(changes)
    DB_SESSION.commit()

def delete_item(item_id, category_id):
    ''' Deletey an item from the database by item_id and category_id '''
    item = get_item(item_id, category_id)
    if item is None:
        msg = '[db]>> Cannot delete non-existant item with id: '
        msg += str(category_id) + '/' + str(item_id)
        print msg
        return False
    else:
        DB_SESSION.delete(item)
        DB_SESSION.commit()
        print '[db]>> Deleted item ' + str(item)
        return True

def delete_items(items):
    ''' Delete all given items in array, calling delete_item() on each.'''
    for item in items:
        DB_SESSION.delete(item)
        print '[db]>> Deleting item ' + str(item)
    DB_SESSION.commit()

def put_category(category):
    ''' Add a new Category to the database. '''
    try:
        DB_SESSION.add(category)
        print '[db]>> Creating category: ' + str(category)
        DB_SESSION.commit()
        return True
    except IntegrityError as error:
        print '[db]>> Error creating category: ' + str(error)
        DB_SESSION.rollback()
        return False

def delete_category(category):
    ''' Delete a given Category from the database. '''
    DB_SESSION.delete(category)
    DB_SESSION.commit()
    print '[db]>> Deleted category ' + str(category)

def get_category(category_id):
    ''' Retrieve a given Category by id from the database. '''
    try:
        category = DB_SESSION.query(Category).filter(Category.category_id == category_id).one()
    except NoResultFound:
        print '[db]>> No category found for id ' + str(category_id)
    return category

def get_items(category_id):
    ''' Get all Items from the database associated/contained in a given
        Category by category_id. '''
    items = DB_SESSION.query(Item).filter(Item.category_id == category_id).all()
    return items

def get_item_count(category_id):
    ''' Get the number of Items assigned to a given category_id '''
    return DB_SESSION.query(Item).filter(Item.category_id == category_id).count()

def get_categories():
    ''' Get all Categories from the database '''
    categories = DB_SESSION.query(Category).all()
    return categories
