#!/usr/bin/python3
"""
SimpleMenu.py
Provides an easy-to-use interface for creating menus with the Curses library.
"""

import curses


class Menu(object):
    def __init__(self, *names, **kwargs):
        # Setup a window object etc., misc Curses stuff.
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()  # No need for [Return]
        curses.noecho()  # Stop keys being printed
        curses.curs_set(0)  # Invisible cursor
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.border(0)


        # Setup color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Setup background
        self.stdscr.bkgd(' ', curses.color_pair(1))

        # Screw this global malarkey
        global y_pos
        y_pos = (self.stdscr.getmaxyx()[0] - len(names)) // 2

        # Create list of menu items
        self.menu_items = []
        for name in names:
            self.menu_items.append(MenuItem(name, self.stdscr))


    def clear_display(self):
        # Restore terminal state to normal.
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        self.stdscr.keypad(False)
        self.stdscr.clear()
        curses.endwin()


    def draw(self):
        # Draw out each item on menu, with highlighting.
        for item in self.menu_items:
            self.stdscr.addstr(item.y_pos, item.x_pos, item.name, item.attr)
        self.stdscr.refresh()


    def start(self):
        try:
            # Initially select first item on the menu.
            selected_item = 0
            self.menu_items[0]._select()
            # Draw out the menu.
            self.draw()
            while True:
                # Get the user's input.
                user_key = self.stdscr.getkey()
                #self.stdscr.addstr(10, 10, user_key)
                #self.stdscr.addstr(11, 10, str(type(user_key)))
                if user_key == "KEY_UP" and selected_item > 0:
                    # Go up one menu item.
                    self.menu_items[selected_item]._deselect()
                    selected_item -= 1
                    self.menu_items[selected_item]._select()
                    self.draw()
                elif (user_key == "KEY_DOWN"
                      and selected_item < len(self.menu_items) - 1):
                    # Go down one menu item.
                    self.menu_items[selected_item]._deselect()
                    selected_item += 1
                    self.menu_items[selected_item]._select()
                    self.draw()
                elif user_key == "\n":
                    # User pressed enter, return choice.
                    self.clear_display()
                    return self.menu_items[selected_item].name        
                elif user_key == "q":
                    self.clear_display()
                    # quit()
                    return None  # Handle this in program.
        except KeyboardInterrupt:
            # Don't throw an error, clear_display() handles restoring terminal state.
            pass

        self.clear_display()


class MenuItem(object):

    def __init__(self, name, stdscr):
        self.name = name
        global y_pos
        self.y_pos = y_pos
        y_pos += 1  # Put each item on a new line.
        maxyx = stdscr.getmaxyx()
        # Horizontally center each line.
        self.x_pos = (maxyx[1] - len(self.name)) // 2
        self.attr = curses.A_NORMAL
    def _select(self):
        # Highlight text.
        self.attr = curses.A_REVERSE
    def _deselect(self):
        # Undo highlight text.
        self.attr = curses.A_NORMAL
