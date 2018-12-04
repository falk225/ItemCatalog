from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    name = Column(String(250), nullable = False)
    id = Column(Integer, primary_key=True)

class Category(Base):
    __tablename__ = 'categories'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'id' : self.id,
            'user_id' : self.user_id
        }

class Item(Base):
    __tablename__ = 'items'

    name = Column(String(80), nullable = False)
    description = Column(String(250))
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'user_id' : self.user_id,
            'category_id' : self.category_id
        }


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)