from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(String, primary_key=True)
    name = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))

    def __str__(self):
        return '<category name:' + self.name + ', id:' + self.id + '>'

class Item(Base):
    __tablename__ = 'item'
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_date = Column(DateTime, server_default=text('NOW()'))
    modified_date = Column(DateTime, server_default=text('NOW()'))
    category_id = Column(String, ForeignKey(Category.id))
    category = relationship(Category)

    def __str__(self):
        s = '<item ['
        s += 'name: ' + self.name + ', '
        s += 'description: ' + self.description + ', '
        s += 'category_id: ' + str(self.category_id) + ' ]>'
        return s