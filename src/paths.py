# These paths are shared across files
import json

file_paths      = 'data/paths.json'                 # Location of stored file paths
log_path        = 'logs/'                    # Location of logs file
rom_info_path   = 'data/rom-info/'                  # Location of rom info
rom_data_path   = 'data/rom_data.json'              # Location of stored rom data
hactool_path    = 'switch/hactool.exe'              # Location of the hactool
prod_keys_path  = 'switch/prod.keys'                # Location of prod.keys
temp_cover_path = 'web/images/temp_cover/cover.png' # Location of temp cover photos
temp_hover_path = 'web/images/temp_hover/hover.png' # Location of temp hover photos

# Grabs the location of the ROM files from the json storing it
def set_roms_path():
    global roms_path

    with open(file_paths, 'r') as f:
        data = json.load(f)
    
    roms_path = data['roms-path']

set_roms_path()