# Imports
import paths, eel, json, rom_entry
from pathlib import Path

# Initialize
eel.init('web')

# List of consoles
console_list = [
            '3DS', 'DS', 'gameboy', 'gameboy-advance', 'gamecube',
            'NES', 'nintendo-64', 'SNES', 'switch', 'wii', 
            'xbox', 'xbox-360'
           ]

# Paths
hashes = 'data/rom-info/'

# Initializes missing data in the JSON files
def add_missing_data():
    default_path_data = ['emulator-paths', 'roms-paths']
    default_rom_data = ['hashed-roms', 'rom-serials', 'switch-games']

    # Creates an empty spot for the path to an emulator .exe
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

        path_options = list(data.keys())
        for path in default_path_data:
            if (path not in path_options):
                data[path] = {}        

        console_paths = list(data['emulator-paths'].keys())

        for console in console_list:
            if console not in console_paths:
                data['emulator-paths'][console.lower()] = ''

        with open(paths.file_paths, 'w') as f:
            json.dump(data, f, indent=4)

    # Creates a folder to store the data of a console
    for console in console_list:
        console_data = Path(hashes + console.lower())
        console_data.mkdir(exist_ok = True)

    # Adds missing starter data to ROMs
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        rom_options = list(data.keys())
        for rom in default_rom_data:
            if (rom not in rom_options):
                data[rom] = {}

        with open(paths.rom_data_path, 'w') as f:
            json.dump(data, f, indent=4)

add_missing_data()

import hashing, consoles, games

# List of games
game_list = []

# Dummy data
for i in range(25):
    game_list.append(f'Game {i}')

# Passes consoles
@eel.expose
def get_consoles():
    return console_list

@eel.expose
def get_games():
    return game_list

# Swaps to the main page after loading is finished
@eel.expose
def reroute_to_main():
    eel.show('index.html')

# Run the program
if __name__ == '__main__':
    eel.start('loading.html', host='localhost', port='5600', size=(1500, 1080))