import threading
import os
from utils import fonts,bprint, install_package, is_numeric, safe_eval
# Try importing the required packages
libraries_list = ["keyboard", "pyperclip","numexpr"]
# Try importing the required packages
for lib in libraries_list:
    print(lib)
    try:
        exec(f"import {lib}")
    except ImportError:
        print(f"{lib} library not found. Installing...")
        install_package(lib)
        exec(f"import {lib}")

# Global flag to indicate whether to quit the program
quit_program = False

# Function to monitor for 'q' key press
def monitor_quit_key():
    global quit_program
    while not quit_program:
        if keyboard.is_pressed('q'):
            print("\nQuitting the session.")
            os._exit(0) # stop the thread

# Function to calculate the Present Value Annuity (PVA) factor
def calculate_pva_factor(years, interest_rate, pv = ''):
    r = interest_rate / 100
    n = 1  # Assuming compounding once per year
    pva_factor = round((1 - (1 + r / n) ** (-years * n)) / (r / n),3)
    if pv:
        print(f'calculated the full pva formula (pv * PVA(n={years},r={interest_rate})) : {pv:,.3f} * {pva_factor}')
        result = f"{pv * (pva_factor):,.3f}"
    else:
        print(f'calculated the pva factor (PVA = PVA(n={years},r={interest_rate})): {pva_factor:,.3f}')
        result = f"{pva_factor:,.3f}"
    return result

# Function to calculate the Future Value Annuity (FVA) factor
def calculate_fva_factor(years, interest_rate, pv = ''):
    if pv:
        print(f'what:{pv}')
    # Assuming the payments are made at the end of each period (ordinary annuity)
    r = interest_rate / 100
    n = 1  # Assuming compounding once per year
    fva_factor = round(((1 + r/n) ** (years * n) - 1) / (r/n),3)
    if pv:
        print(f'calculated the full fva formula (pv * FVA(n={years},r={interest_rate})) : {pv:,.3f} * {fva_factor}')
        result = f"{pv * (fva_factor):,.3f}"
    else:
        print(f'calculated the fva factor (FVA = PVA(n={years},r={interest_rate})): {fva_factor:,.3f}')
        result = f"{fva_factor:,.3f}"
    return result

# Main function
def formula_handler(formula_name):
    # clear all content
    os.system('cls')
    # open new thread for `monitor_quit_key` function
    threading.Thread(target=monitor_quit_key, daemon=True).start()
    bprint(f"{formula_name} formula:",'bold')
    bprint(f"* enter `Q` any time to stop the session",'info')
    while not quit_program:
        # show the error messgae only after the second loop (we decalre those variables later on so use that...)
        if 'years' in locals() and 'interest_rate' in locals():
            bprint("INVALID INPUT, PLEASE TRY AGAIN", 'error')
        bprint("* please enter only numbers!", 'warning')
        years = input("Enter period (in years):\n")
        interest_rate = input("Enter interest rate:\n")
        bprint('* Here you can use number (e.g: 16.5) or mathematical expression (e.g: 12 * 9520)','warning')
        value = input(f"Enter {'present' if (formula_name == 'PVA') else 'future'} value (optional, press `enter` if you don't want this paramater):\n")
        value = safe_eval(value) # let the user the option to write mathematical expression or number
        if quit_program:  # Check if quit flag is set
            os._exit(0)
            return
        if is_numeric(years) and is_numeric(interest_rate):
            years = float(years)
            interest_rate = float(interest_rate)
            value = float(value) if (value and is_numeric(value)) else value
            if formula_name == 'PVA':
                formula_factor = calculate_pva_factor(years, interest_rate, value)
            elif formula_name == 'FVA':
                formula_factor = calculate_fva_factor(years, interest_rate, value)
            bprint(f"* The {formula_name} factor copied to your cilpboard",'info')
            bprint(f"{formula_name} factor for {years} years at {interest_rate}% interest rate: {fonts['BOLD']}{formula_factor}{fonts['RESET']}",'success')
            # Copy the value to the clipboard
            pyperclip.copy(formula_factor)
            return