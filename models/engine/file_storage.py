#!/usr/bin/python
"""
This is a module that contain a class template
that serializes instances to a JSON file and
deserializes JSON file to instances
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """
    serializes instances to a JSON file
    and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}
    # __serializable_dict = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        obj_id = obj.id
        obj_class = obj.__class__.__name__
        obj_key = obj_class + "." + obj_id
        FileStorage.__objects[obj_key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w', encoding="utf-8") as f:
            py_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(py_dict, f, indent=4)


    def reload(self):
        """
        deserializes the JSON file to __objects
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                json_obj = json.load(f)
                for k, v in json_obj.items():
                      obj =  eval(v["__class__"])(**v)
                      FileStorage.__objects[k] = obj 
        except:
            pass
