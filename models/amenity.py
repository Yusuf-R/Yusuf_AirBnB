#!/usr/bin/python3
"""
This template for the User class
"""
from .base_model import BaseModel


class Amenity(BaseModel):
    """
    User class
    """
    name = ""

    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        super().__init__(*args, **kwargs)
        return
