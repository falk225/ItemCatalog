from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# class Base(declarative_base):
#     __abstract__ = True
#     id            = Column(db.Integer, primary_key=True)
#     date_created  = Column(db.DateTime,  default=func.current_timestamp())
#     date_modified = Column(db.DateTime,  default=func.current_timestamp(),
#                                            onupdate=func.current_timestamp())

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    google_id = Column(Integer, nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
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
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    
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