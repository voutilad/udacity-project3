from database_setup import Category, Item, session


def getItem(item_id):
    s = session()
    item = s.query(Item).filter(Item.id == item_id).one()
    s.close()
    return item

def putItem(item):
    s = session()
    s.add(item)
    print 'Creating new item: ' + str(item)
    s.commit()
    s.close()

def deleteItem(item_id):
    item = getItem(item_id)
    if item is None:
        print 'Cannot delete non-existant item with id: ' + str(item_id)
    else:
        s = session()
        s.delete(item)
        s.flush()
        s.commit()
        s.close()
        print 'Deleted item ' + str(item)


def getCategory(category_id):
    s = session()
    category = s.query(Category).filter(Category.id == category_id).one()
    s.close()
    return category

def getItems(category_id):
    s = session()
    items =  s.query(Item).filter(Item.category_id == category_id).all()
    s.close()
    return items

def getCategories():
    s = session()
    categories = s.query(Category).all()
    s.close()
    return categories
