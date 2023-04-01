#!/usr/bin/python3
"""
This module contains a class
that creates a command line interpreter
"""
import json
import cmd
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
import re


class HBNBCommand(cmd.Cmd):
    """
    A simple command line interface for the AirBnB Project.
    """
    valid_class = {
            'BaseModel': BaseModel, 'User': User, 'City': City,
            'State': State, 'Amenity': Amenity, 'Place': Place,
            'Review': Review
            }
    exempt_attrib = ["id", "created_at", "updated_at"]
    console_cmds = ['all', 'count', 'show', 'destroy', 'update']
    spec1_cmds = ['count', 'all']
    spec2_cmds = ['show', 'destroy']

    def __init__(self):
        """
        The constructor for HBNBCommand class.
        """
        super().__init__()
        self.prompt = '(hbnb) '

    def do_quit(self, line):
        """Quits the console program."""
        return True

    def help_quit(self):
        """quit documentation"""
        print("Syntax: quit")
        print("Terminates and exit the program")

    def do_EOF(self, line):
        """
        Terminates and exit from the console program
        """
        print("Exiting...\nDone")
        return True

    def help_EOF(self):
        """EOF documenataion"""
        print("Syntax: Ctrl + D")
        print("Terminates the program")

    def emptyline(self):
        """
        Ignores empty lines
        """
        pass

    def help_emptyline(self):
        """emptyline doucmentation"""
        print("Ignores empty lines")

    def do_create(self, line):
        """
        Creates a new instance of BaseModel
        """
        if line == "":
            print("** class name missing **")
            return
        if line not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return
        else:
            new_instance = HBNBCommand.valid_class[line]()
            new_instance.save()
            print(new_instance.id)

    def help_create(self):
        """
        Creates a new class instance
        """
        print("Creates a new instance of the class")

    def do_show(self, line):
        """
        Prints the string representation of an instance
        """

        if line == "":
            print("** class name missing **")
            return

        line_vector = line.split()
        if line_vector[0] not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return
        if len(line_vector) < 2:
            print("** instance id missing **")
            return

        stored_obj = FileStorage().all()

        line_key = line_vector[0] + "." + line_vector[1]
        if line_key not in stored_obj:
            print("** no instance found **")
            return
        obj = stored_obj[line_key]
        print(obj)

    def help_show(self):
        """
        Prints the string representation of an instance
        """
        print("Prints the string representation of an instance")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        """
        line_vector = line.split()

        if len(line_vector) == 0:
            print("** class name missing **")
            return
        if line_vector[0] not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return
        if len(line_vector) < 2:
            print("** instance id missing **")
            return
        stored_obj = FileStorage().all()

        line_key = line_vector[0] + "." + line_vector[1]
        if line_key not in stored_obj:
            print("** no instance found **")
            return
        del stored_obj[line_key]
        FileStorage().save()

    def do_all(self, line):
        """
        Prints all string representation of all instances
        """
        line_vec = line.split()
        str_list = []
        stored_dict_of_object = FileStorage().all()

        if len(line_vec) == 0:
            str_list = [v.__str__() for _, v in stored_dict_of_object.items()]
            print(str_list)
            return

        if line_vec[0] not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return

        if line in HBNBCommand.valid_class:
            str_list = [v.__str__() for _, v in stored_dict_of_object.items()
                        if v.__class__.__name__ == line]
            print(str_list)
            return

    def do_update(self, line):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute
        """
        if not line:
            print("** class name missing **")
            return
        get_line = re.match(r"""'?"?(.*)"?'?""", line)
        if get_line:
            get_line = get_line.group(1)
        grp_input = line.split()
        grp_cls = grp_input[0]
        if grp_cls not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return
        if len(grp_input) < 2:
            print("** instance id missing **")
            return
        grp_id = grp_input[1]
        stored_obj = FileStorage().all()
        stored_dict_key = grp_cls + "." + grp_id
        if stored_dict_key not in stored_obj:
            print("** no instance found **")
            return
        if len(grp_input) < 3:
            print("** attribute name missing **")
            return
        if len(grp_input) < 4:
            print("** attribute value missing **")
            return
        attr_filter = line.partition(" ")[2]
        grp_attr = attr_filter.partition(" ")[2]

        if grp_attr[0] not in ["\"", "{", "\'"]:
            pattern = r'^(\S+)\s+("[^"]+"|\'[^\']+\'|\S+).*'
            obj = stored_obj[stored_dict_key]
            grp = re.search(pattern, grp_attr)
            if grp is None:
                return
            attr_name = grp.group(1)
            if attr_name.endswith(","):
                attr_name = attr_name[:-1]
            if attr_name in HBNBCommand.exempt_attrib:
                print("** cannot update this attribute **")
                return
            attr_val = grp.group(2)
            if attr_val[0] in ["\"", "\'"]:
                attr_val = attr_val[1:-1]
            try:
                if int(attr_val):
                    setattr(obj, attr_name, int(attr_val))
                    obj.save()
                    return
            except Exception:
                try:
                    if float(attr_val):
                        setattr(obj, attr_name, float(attr_val))
                        obj.save()
                        return
                except Exception:
                    setattr(obj, attr_name, attr_val)
                    obj.save()
                    return

        elif grp_attr[0] in ["\"", "\'"]:
            pattern = r'["\']?([^"\']*)["\']?[,\s]*["\']?([^"\']*)["\']?'
            # match only first and second string
            grp = re.search(pattern, grp_attr)
            if grp is None:
                return
            attr_name = grp.group(1).strip()
            if attr_name in HBNBCommand.exempt_attrib:
                print("** cannot update this attribute **")
                return
            attr_val = grp.group(2).strip()
            obj = stored_obj[stored_dict_key]
            try:
                if int(attr_val):
                    setattr(obj, attr_name, int(attr_val))
                    obj.save()
                    return
            except Exception:
                try:
                    if float(attr_val):
                        setattr(obj, attr_name, float(attr_val))
                        obj.save()
                        return
                except Exception:
                    setattr(obj, attr_name, attr_val)
                    obj.save()
                    return

        elif grp_attr[0] == "{":
            json_ready = grp_attr
            json_obj = json_ready.replace("'", '"')
            pyt_obj = json.loads(json_obj)
            for key, value in pyt_obj.items():
                if key in HBNBCommand.exempt_attrib:
                    print("** cannot update this attribute **")
                    return
                attr_name = key
                attr_val = value
                obj = stored_obj[stored_dict_key]
                try:
                    if int(attr_val):
                        setattr(obj, attr_name, int(attr_val))
                        obj.save()
                except Exception:
                    try:
                        if float(attr_val):
                            setattr(obj, attr_name, float(attr_val))
                            obj.save()
                    except Exception:
                        setattr(obj, attr_name, attr_val)
                        obj.save()

    def help_update(self):
        """update the object attribute"""
        print("""Updates an instance based on the class name
              and id by adding or updating attribute""")

    def default(self, line):
        """
        This method called on an input line when
        the command prefix is not recognized
        """
        ukn_prefix = self.input_refactored(line)
        if ukn_prefix == line:
            print("** This command is outrageously unknown **")
            return

    def input_refactored(self, line):
        """Will try to reassemble the syntax passed and make sense out of it"""
        pattern = r'^(\w*)\.(\w+)(?:\(([^)]*)\))$'
        grp = re.search(pattern, line)
        if not grp:
            return line
        grp_class = grp.group(1)
        grp_console_cmd = grp.group(2)
        grp_args = grp.group(3)

        if grp_class not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return
        if grp_console_cmd not in HBNBCommand.console_cmds:
            print("** console command doesn't exist **")
            return
        if len(grp_args) == 0 and grp_console_cmd in HBNBCommand.spec1_cmds:
            syntax_refactored = grp_console_cmd + " " + grp_class
            self.onecmd(syntax_refactored)
            return syntax_refactored
        if len(grp_args) > 0 and grp_console_cmd in HBNBCommand.spec2_cmds:
            id_syntax = grp_args[1:-1]
            syntax_refactored = (grp_console_cmd + " " + grp_class +
                                 " " + id_syntax)
            self.onecmd(syntax_refactored)
            return syntax_refactored
        if len(grp_args) > 0 and grp_console_cmd == "update":
            update_syntax = grp_args.partition(",")
            id_syntax = update_syntax[0]
            id_syntax = id_syntax[1:-1]
            update_syntax = update_syntax[2].strip()

            if update_syntax[0] != "{":
                pattern = r'["\']?([^"\']*)["\']?[,\s]*["\']?([^"\']*)["\']?'
                # match only first and second string
                grp = re.search(pattern, update_syntax)
                if grp is None:
                    return line
                attr_name = grp.group(1).strip()
                if attr_name.endswith(","):
                    attr_name = attr_name[:-1]
                attr_name = '"' + attr_name + '"'
                attr_val = grp.group(2).strip()
                attr_val = '"' + attr_val + '"'
                syntax_refactored = (grp_console_cmd + " " + grp_class +
                                     " " + id_syntax + " " + attr_name +
                                     " " + attr_val)
                print(syntax_refactored)
                self.onecmd(syntax_refactored)
                return syntax_refactored

            if update_syntax[0] == "{":
                dict_syntax = update_syntax
                syntax_refactored = (grp_console_cmd + " " + grp_class +
                                     " " + id_syntax + " " + dict_syntax)
                self.onecmd(syntax_refactored)
                return syntax_refactored
            else:
                return line
        else:
            return line

    def do_count(self, line):
        """
        Counts the number of instances of a class
        """
        line_vector = line.split()
        cls_count = 0
        stored_dict_of_object = FileStorage().all()

        if len(line_vector) == 0:
            for _ in stored_dict_of_object:
                cls_count += 1
            print(cls_count)
            return
        if line_vector[0] not in HBNBCommand.valid_class:
            print("** class doesn't exist **")
            return

        grp_cls = line_vector[0]
        for _, v in stored_dict_of_object.items():
            if v.__class__.__name__ == grp_cls:
                cls_count += 1
        print(cls_count)
        return

    def help_count(self):
        """Counts the number of instances of a class"""
        print("""Counts the number of instances of a class""")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
