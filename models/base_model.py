#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs.setdefault('id', str(uuid4()))
        kwargs.setdefault('created_at', datetime.utcnow())
        if not isinstance(kwargs['created_at'], datetime):
            kwargs['created_at'] = datetime.strptime(
                kwargs['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        kwargs.setdefault('updated_at', datetime.utcnow())
        if not isinstance(kwargs['updated_at'], datetime):
            kwargs['updated_at'] = datetime.strptime(
                kwargs['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
