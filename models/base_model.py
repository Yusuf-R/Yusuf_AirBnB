#!/usr/bin/python3
"""
This module defines all common attributes/methods for other classes:
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    This class defines all common attributes/methods for other classes:

    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel
        """
        if kwargs:
            dt_fmt = "%Y-%m-%dT%H:%M:%S.%f"
            date_obj = ["created_at", "updated_at"]

            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in date_obj:
                    value = datetime.strptime(value, dt_fmt)
                setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current
        datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
