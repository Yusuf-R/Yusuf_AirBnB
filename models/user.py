#!/usr/bin/python3
"""
This template for the User class
"""
from .base_model import BaseModel


class User(BaseModel):
    """
    User class
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        super().__init__(*args, **kwargs)
        return
