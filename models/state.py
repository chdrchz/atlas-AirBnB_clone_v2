#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", 
                          cascade="all, delete, delete-orphan")
    @property
    def cities(self):
        """" Returns the list of City instances with state_id. """
        import models
        from models.city import City
        city_list = []
        all_cities = models.storage.all(models.City)
        for city in all_cities.values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
