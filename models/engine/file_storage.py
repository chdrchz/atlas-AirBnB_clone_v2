#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import inspect
import json
from models import city, place, review, state, amenity, user, base_model


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    CDIC = {
            'City': city.City,
            'Place': place.Place,
            'Review': review.Review,
            'State': state.State,
            'Amenity': amenity.Amenity,
            'User': user.User
        }

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        classes = self.CDIC
        for class_name, class_obj in classes.items():
            if cls is None or cls is class_obj or cls is class_name:
                objs = self.__session.query(class_obj).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        obj_dict = obj.to_dict()
        if '__class__' in obj_dict:
            key = obj_dict['__class__'] + '.' + obj.id
            self.all().update({key: obj})
        else:
            print("Error: '__class__' key not found in object dictionary.")

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Woah new public instances. """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Handles closing the session"""
        self.reload()
