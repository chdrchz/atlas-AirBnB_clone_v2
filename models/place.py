from sqlalchemy import Table
import os
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class Place(BaseModel, Base):
    """ Place inherits from BaseModel and Base and a nice place to stay. """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Establishing the relationship with Amenity
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    # For DBStorage
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                              Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
                              )

    # For FileStorage
    if os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def amenities(self):
            """ Getter attribute amenities that returns the list of Amenity instances """
            amenities_list = []
            from models import storage
            all_amenities = storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute amenities that handles appending Amenity.id """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
