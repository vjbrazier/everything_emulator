# These paths are shared across files

import json

file_paths = 'data/paths.json'  # Location of stored file paths
rom_info_path = 'data/rom-info/' # Location of rom info
rom_data_path = 'data/rom_data.json' # Location of stored rom data

# Grabs the location of the ROM files from the json storing it
def set_roms_path():
    global roms_path

    with open(file_paths, 'r') as f:
        data = json.load(f)
    
        roms_path = data['roms-path']

set_roms_path()