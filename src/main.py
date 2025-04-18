# Imports
import paths
import eel
import json
import os
from pathlib import Path

# Get the absolute path to the folder where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Set Eel to use that exact folder as the root
eel.init(base_dir)
main_window_open = False

# List of consoles
console_list = [
            '3DS', 'DS', 'gameboy', 'gameboy-advance', 'gamecube',
            'NES', 'nintendo-64', 'SNES', 'switch', 'wii', 
            'xbox', 'xbox-360'
           ]

# Initializes missing data in the JSON files
def add_missing_data():
    default_path_data = ['emulator-paths', 'roms-paths']

    # Creates an empty spot for the path to an emulator .exe
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    for path in default_path_data:
        data.setdefault(path, {})       

    for console in console_list:
        data['emulator-paths'].setdefault(console.lower(), '')

    with open(paths.file_paths, 'w') as f:
        json.dump(data, f, indent=4)

    # Creates a folder to store the data of a console
    for console in console_list:
        (Path(paths.rom_info_path) / console.lower()).mkdir(exist_ok=True)

add_missing_data()

# Not used within the file, but are imported so that all the code within is loaded
import hashing, consoles, games, rom_entry

# Passes consoles
@eel.expose
def get_consoles():
    return console_list

@eel.expose
def change_main_window_status():
    global main_window_open

    main_window_open = False

# Swaps to the main page after loading is finished
@eel.expose
def reroute_to_main():
    global main_window_open

    if not main_window_open:
        eel.show('web/index.html')
        main_window_open = True

# Run the program
if __name__ == '__main__':
    eel.start('web/loading.html', host='localhost', port='5600', size=(1500, 1080))