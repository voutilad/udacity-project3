from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __str__(self):
        return '<category name:' + self.name + ', id:' + self.id + '>'

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category)

    def __str__(self):
        s = '<item ['
        s += 'name: ' + self.name + ', '
        s += 'description: ' + self.description + ', '
        s += 'category_id: ' + str(self.category_id) + ' ]>'
        return s
