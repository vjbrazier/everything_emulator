# Imports
import paths
import eel
import json
import hashing
import time
import threading
import tkinter as tk
from tkinter import filedialog

# Updates the path to the roms in the JSON file
def update_rom_path(file_path):
    if not file_path:
        return

    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    data['roms-path'] = file_path + '/'

    with open(paths.file_paths, 'w') as f:
        json.dump(data, f, indent=4)

    # Reloads all the roms following a path change in case new ones were added
    paths.set_roms_path()
    time.sleep(1) # A brief pause to ensure that the rom_path is set prior to attempting to read it
    eel.show('loading.html')
    time.sleep(1) # Similar to above
    eel.close_window()

# @eel.expose
# def begin_rom_hashing():
#     hashing.rom_analysis()

# Opens the file explorer for the user to select the rom folder
@eel.expose
def modify_rom_path():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_path = filedialog.askdirectory(parent = root, title = 'Select the rom folder')

    try:
        update_rom_path(file_path)
    except:
        print("You didn't seem to choose a folder.")

    root.destroy()

# Loads games that have been logged in the data to 