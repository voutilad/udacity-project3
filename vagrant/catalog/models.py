'''
Data model for Catalog application leveraging sqlalchemy conventions
'''
from sqlalchemy import Column, ForeignKey, String, DateTime, text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import BASE

class Category(BASE):
    ''' Category for organizing one or many Items '''
    __tablename__ = 'category'
    category_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))

    def __init__(self, category_id=None, name=None, description=None):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.created_date = datetime.now()
        self.modified_date = datetime.now()

    def __str__(self):
        string = '<category name:' + self.name
        string += ', category_id:' + self.category_id
        string += ', description: ' + self.description + '>'
        return string

    def to_json(self):
        ''' Return JSON for Category '''
        return {'category_id':self.category_id,
                'name':self.name,
                'description':self.description,
                'created_date':self.created_date,
                'modified_date':self.modified_date}

    def update_modified_date(self):
        ''' Update the modified date setting it to current time on server. '''
        self.modified_date = datetime.now()

class Item(BASE):
    ''' Base unit of thing contained inside a Category. '''
    __tablename__ = 'item'
    item_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))
    category_id = Column(String, ForeignKey(Category.category_id), primary_key=True)
    category = relationship(Category)

    def __init__(self, item_id=None, name=None, description=None, category_id=None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.created_date = datetime.now()
        self.modified_date = datetime.now()

    def __str__(self):
        pattern = '<item [name: {name}, item_id: {item_id}, '
        pattern = pattern + 'description: {description}, category_id: {category_id}]>'
        return pattern.format(name=self.name,
                              item_id=self.item_id,
                              description=self.description,
                              category_id=str(self.category_id))


    def to_json(self):
        ''' Serialize Item to JSON '''
        return {'item_id':self.item_id, 'name':self.name,
                'description':self.description,
                'created_date':self.created_date,
                'modified_date':self.modified_date,
                'category_id':self.category_id}

    def update_modified_date(self):
        ''' Update modified date of Item, setting to current server time. '''
        self.modified_date = datetime.now()

class User(BASE):
    ''' User account associated with supported cloud auth services '''
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    picture = Column(String)
    service = Column(String)

    def __init__(self, user_id=None, name=None, email=None,
                 picture=None, service=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.picture = picture
        self.service = service
