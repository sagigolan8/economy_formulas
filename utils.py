
import subprocess
import sys

# ANSI escape codes
global fonts
fonts = {
    'YELLOW' : '\033[33m', # Yellow text
    'CYAN' : '\033[36m',   # Cyan text
    'RESET' : '\033[0m',  # Reset to default color
    'BOLD' : '\033[1m',   # Bold text
    'RED' : '\033[31m',  # Red text
    'GREEN' : '\033[32m' # Green text
}

# Function to install a package using pip
def install_package(package):
    # Run the pip install command to install the specified package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

libraries_list = ["keyboard", "pyperclip","numexpr"]
# Try importing the required packages
for lib in libraries_list:
    try:
        exec(f"import {lib}")
    except ImportError:
        print(f"try importing - {lib} library")
        print(f"{lib} library not found. Installing...")
        install_package(lib)
        exec(f"import {lib}")

def is_numeric(str):
    # Check if the string is empty
    if not str:
        return False
    # Try to convert the string to a float
    try:
        num = float(str)
    except ValueError:
        return False
    # Check if the number is positive
    return num >= 0

# beautiful print
def bprint(msg,type):
    if type == 'error':
        print(f'{fonts["RED"]}{fonts["BOLD"]}{msg}{fonts["RESET"]}')
    elif type == 'warning':
        print(f'{fonts["YELLOW"]}{fonts["BOLD"]}{msg}{fonts["RESET"]}')
    elif type == 'info':
        print(f'{fonts["CYAN"]}{fonts["BOLD"]}{msg}{fonts["RESET"]}')
    elif type == 'success':
        print(f'{fonts["GREEN"]}{fonts["BOLD"]}{msg}{fonts["RESET"]}')
    elif type == 'bold':
        print(f'{fonts["BOLD"]}{msg}{fonts["RESET"]}')

def safe_eval(str_expr):
    # Handle invalid numexpr import
    if not numexpr:
        return None
    if not any(char.isalpha() for char in str_expr):
        try:
            # Evaluate the expression using numexpr
            return numexpr.evaluate(str_expr)
        except (SyntaxError, ValueError, TypeError):
            # Handle invalid input
            return None

def user_prompt():
    while True:  # Start an infinite loop
        user_input = input("Do you want to continue? (y/n): ").strip().lower()
        if user_input == 'y':
            return True  # Continue the program
        elif user_input == 'n':
            print("Quitting the session...")
            return False  # Stop the program
        else:
            bprint("Invalid input. Please enter 'y' or 'n'.",'error')
