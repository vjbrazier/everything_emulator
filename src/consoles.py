# Imports
import paths
import eel
import os
import json
import tkinter as tk
from tkinter import filedialog
from custom_logger import add_to_log

# Returns a boolean based on whether or not a path has been set for a console
@eel.expose
def check_path_exists(console):
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    return data['emulator-paths'].get(console, '') != ''

# Opens the file at the path for a console
@eel.expose
def open_console(console):
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    # Prevents opening a .png, for example
    file = data['emulator-paths'][console]
    if file[-4:] != '.exe':
        message = f'[ERROR] You chose an invalid file: {file}'

        add_to_log(message)
        eel.game_open_error(message, '')
        return

    try:
        os.startfile(data['emulator-paths'][console])
    except Exception as e:
        message = f'[ERROR] A problem occurred: {e}'

        add_to_log(message)
        eel.game_open_error(message, '')

# Updates the path to the console in the JSON file
def update_console_path(console, file_path):
    if not file_path:
        return
    
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    add_to_log(f'[INFO] Set emulator path for {console} to {file_path}')
    data['emulator-paths'][console] = file_path

    with open(paths.file_paths, 'w') as f:
        json.dump(data, f, indent=4)

# Opens the file explorer for the user to select the emulator path
@eel.expose
def modify_console_path(console):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        parent = root, 
        title = 'Select the .exe of the emulator'
    )

    update_console_path(console, file_path)

    root.destroy()