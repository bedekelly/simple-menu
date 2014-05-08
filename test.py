#!/usr/bin/python2
from SimpleMenu import Menu

new_menu = Menu("Choice A", "Choice B", "Choice C")
choice = new_menu.start()

if choice is not None:
    print("You chose {}.".format(choice))
else:
    print("Exiting program now.")
