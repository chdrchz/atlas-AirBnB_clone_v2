#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone
with new SQL database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
import os


class DBStorage:
    """
    Handles long-term storage of all class instances via SQLAlchemy ORM.
    Thank you Doug.
    """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes the database engine. """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.environ['HBNB_MYSQL_USER'],
                                             os.environ['HBNB_MYSQL_HOST'],
                                             os.environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Queries all objects of a given class from the database. """
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls).all()
            for obj in query:
                key = f'{obj.__class__.__name__}.{obj.id}'
                objects[key] = obj
        else:
            from models.state import State
            from models.city import City
            classes = [State, City]
            for cls in classes:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    objects[key] = obj
        return objects

    def new(self, obj):
        """ Adds a new object to the session. """
        self.__session.add(obj)

    def save(self):
        """ Commits changes to the database. """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes an object from the session. """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates database tables and initializes a new session. """
        from models.state import State
        from models.city import City
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = Session()
