#!/usr/bin/python3
"""
This template for the User class
"""
from .base_model import BaseModel
from .state import State


class City(BaseModel):
    """
    User class
    """
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        super().__init__(*args, **kwargs)
        City.state_id = State().id
        return
