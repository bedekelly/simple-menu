#!/usr/bin/python3
from SimpleMenu import Menu

new_menu = Menu("Choice A",
				"Choice B",
				"Choice C",
				title="Title",
				subtitle="Subtitle (Press Q to quit)")

choice = new_menu.show()

if choice is not None:
    print("You chose {}.".format(choice))
else:
    print("You quit the program.")
