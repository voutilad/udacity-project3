'''
Data model for Catalog application leveraging sqlalchemy conventions
'''
from sqlalchemy import Column, ForeignKey, String, DateTime, text
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))

    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        s = '<category name:' + self.name + ', id:' + self.id
        s = s + ', description: ' + self.description + '>'
        return s

    def to_json(self):
        return {'id':self.id, 'name':self.name, 'description':self.description,
                'created_date':self.created_date, 'modified_date':self.modified_date}

class Item(Base):
    __tablename__ = 'item'
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))
    category_id = Column(String, ForeignKey(Category.id), primary_key=True)
    category = relationship(Category)

    def __init__(self, id=None, name=None, description=None, category_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.category_id = category_id

    def __str__(self):
        pattern = '<item [name: {name}, id: {id}, '
        pattern = pattern + 'description: {description}, category_id: {category_id}]>'
        return pattern.format(name=self.name,
                              id=self.id,
                              description=self.description,
                              category_id=str(self.category_id))


    def to_json(self):
        return {'id':self.id, 'name':self.name,
                'description':self.description,
                'created_date':self.created_date,
                'modified_date':self.modified_date,
                'category_id':self.category_id}

class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    picture = Column(String)

    def __init__(self, user_id=None, name=None, email=None, picture=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.picture = picture
