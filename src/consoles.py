# Imports
import paths, eel, os, json, tkinter as tk
from tkinter import filedialog

# Returns a boolean based on whether or not a path has been set for a console
@eel.expose
def check_path_exists(console):
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

        if (data['emulator-paths'][console] != ''):
            return True
        else:
            return False

# Opens the file at the path for a console
@eel.expose
def open_console(console):
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

        try:
            os.startfile(data['emulator-paths'][console])
        except:
            eel.error_message()

# Updates the path to the console in the JSON file
def update_console_path(console, file_path):
    if (file_path):
        with open(paths.file_paths, 'r') as f:
            data = json.load(f)

            data['emulator-paths'][console] = file_path

        with open(paths.file_paths, 'w') as f:
            json.dump(data, f, indent=4)

# Opens the file explorer for the user to select the emulator path
@eel.expose
def modify_console_path(console):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_path = filedialog.askopenfilename(parent = root, title = 'Select the .exe of the emulator')

    try:
        update_console_path(console, file_path)
    except:
        print("You didn't seem to choose a file.")

    root.destroy()