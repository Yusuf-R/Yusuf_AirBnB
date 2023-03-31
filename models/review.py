#!/usr/bin/python3
"""
This template for the User class
"""
from .base_model import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    """
    User class
    """
    place_id = ""
    user_id = ""
    text = ""
    
    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        super().__init__(*args, **kwargs)
        Review.place_id = Place().id
        Review.user_id = User().id

        return
