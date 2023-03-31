#!/usr/bin/python3
"""
This module contains a class
that creates a command line interpreter
"""

import cmd
import readline


class Console(cmd.Cmd):
    """
    A simple command line interface for the AirBnB Project.
    """
    prompt = '(hbnb) '

    def do_greet(self, line):
        """
        Greets the user
        """
        if line and line == "Chee-zee":
            print("Hi Martian {}, Welcome to the cosmos!".format(line))
        elif line:
            print("Hi {}, Welcome to the console".format(line))
        else:
            print("Hi ALX_SE fellow")

    def do_EOF(self, line):
        """
        Exits the program
        """
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

if __name__ == "__main__":
    Console().cmdloop()
