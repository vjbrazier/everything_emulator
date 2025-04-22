# Imports
import paths
import eel
import json
import os
from pathlib import Path
from custom_logger import add_to_log

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
    # Creates an empty spot for the path to an emulator .exe
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    if 'emulator-paths' not in data:
        add_to_log(f'[INFO] emulator-paths is missing from JSON, adding...')
        data['emulator-paths'] = {}

    if 'roms-path' not in data:
        add_to_log(f'[INFO] roms-path is missing from JSON, adding...')
        data['roms-path'] = ''
        paths.set_roms_path()

    for console in console_list:
        if console.lower() not in data['emulator-paths']:
            add_to_log(f'[INFO] {console} is missing from JSON, adding...')
        
        data['emulator-paths'].setdefault(console.lower(), '')

    with open(paths.file_paths, 'w') as f:
        add_to_log(f'[INFO] Writing changes to JSON...')
        json.dump(data, f, indent=4)

    # Creates a folder to store the data of a console
    for console in console_list:
        if not os.path.exists(Path(paths.rom_info_path) / console.lower()):
            add_to_log(f'[INFO] Folder for {console} is missing, creating...')
        
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
        add_to_log(f'[INFO] Rerouting to main page')
    
        eel.show('web/index.html')
        main_window_open = True

# Run the program
if __name__ == '__main__':
    add_to_log(f'[INFO] Starting application')
    eel.start('web/loading.html', host='localhost', port='5600', size=(1500, 1080))