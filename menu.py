import platform
import os
from formula import formula_handler
from utils import install_package, user_prompt

# Check if the operating system is Windows
if platform.system() == 'Windows':
    # Try importing the windows-curses package
    try:
        import curses
    except ImportError:
        print("curses library not found. Installing windows-curses, please wait...")
        install_package('windows-curses')
        print("curses library installed successfully.")
        # Import curses again after installation
        import curses
else:
    import curses

# List of options to be displayed in the menu
formula_list = ['PVA', 'FVA', 'Exit']

# Title of the menu
title = "Choose formula"

# Function to draw the menu
def show_menu(stdscr, selected_row_idx):
    """ Draw the menu with options on the screen. """
    # Clear the screen before drawing the menu
    stdscr.clear()
    # Get the height and width of the screen
    h, w = stdscr.getmaxyx()

    # Calculate the x and y coordinates to center the title
    x_cord = (w - len(title)) // 2
    y_cord = h // 4  # Placing the title at one-fourth the screen height

    # Add the title to the screen at the calculated position
    stdscr.addstr(y_cord, x_cord, title)

    # Loop through the list of options and display them
    for index, row in enumerate(formula_list):
        # Calculate x and y positions for each option to center them
        x = w // 2 - len(row) // 2
        y = h // 2 - len(formula_list) // 2 + index
        # Highlight the selected option
        if index == selected_row_idx:
            stdscr.attron(curses.color_pair(1))  # Turn on the color pair for highlighting
            stdscr.addstr(y, x, row)  # Add the highlighted option to the screen
            stdscr.attroff(curses.color_pair(1))  # Turn off the color pair
        else:
            # Add non-selected options normally
            stdscr.addstr(y, x, row)

    # Refresh the screen to update the changes
    stdscr.refresh()

# Main menu function
def menu_handler(stdscr):
    """ Main function to handle the menu functionality. """
    # Hide the cursor for better aesthetics
    curses.curs_set(0)
    # Initialize color pair 1 for highlighting selected option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Initialize the index of the currently selected row
    current_row_idx = 0
    # Draw the initial menu
    show_menu(stdscr, current_row_idx)
    # Flag to control the menu loop
    exit_menu = False

    while not exit_menu:
        # Get user key press
        key = stdscr.getch()

        # Navigate up in the menu
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        # Navigate down in the menu
        elif key == curses.KEY_DOWN and current_row_idx < len(formula_list) - 1:
            current_row_idx += 1
        # Select an option with the Enter key
        elif key == curses.KEY_ENTER or key in [10, 13]:
            formula_name = formula_list[current_row_idx]
            # Check if the selected option is 'exit'
            if formula_name == "Exit":
                exit_menu = True
                # clear all content
                break  # Exit the menu
            else:
                # Temporarily exit curses mode to perform standard I/O operations
                curses.endwin()
                try:
                    os.system('cls')
                    # Call the handler function (which might use input())
                    formula_handler(formula_name)
                    if not user_prompt():
                        os._exit(0)
                    os.system('cls')
                finally:
                    # Reinitialize curses environment after non-curses I/O is done
                    stdscr = curses.initscr()
                    curses.noecho()
                    curses.cbreak()
                    stdscr.keypad(True)
                    # Redraw the menu
                    show_menu(stdscr, current_row_idx)
        if not exit_menu:
            # Redraw the menu with the updated selected row
            show_menu(stdscr, current_row_idx)

# Run the program
curses.wrapper(menu_handler)
