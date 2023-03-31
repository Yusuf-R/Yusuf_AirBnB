#!/usr/bin/python3
"""
This template for the User class
"""
from .base_model import BaseModel
from .user import User
from .city import City
from .amenity import Amenity


class Place(BaseModel):
    """
    User class
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
    
    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        super().__init__(*args, **kwargs)
        Place.city_id = City().id
        Place.user_id = User().id
        Place.amenity_ids = Place.amenity_ids.append(Amenity().id)

        return
