# Imports
import paths, eel, json, hashing, consoles, games
from pathlib import Path

# Initialize
eel.init('web')

# List of consoles
console_list = [
            '3DS', 'DS', 'gameboy', 'gameboy-advance', 'gamecube',
            'NES', 'nintendo-64', 'playstation', 'playstation-2', 'sega-genesis',
            'SNES', 'switch', 'wii', 'wii-U', 'xbox',
            'xbox-360'
           ]

# Paths
hashes = 'data/rom-info/'

# Initializes missing data in the paths file
def add_missing_data():

    # Creates an empty spot for the path to an emulator .exe
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

        console_paths = list(data['emulator-paths'].keys())

        for console in console_list:
            if console not in console_paths:
                data['emulator-paths'][console] = ''

        with open(paths.file_paths, 'w') as f:
            json.dump(data, f, indent=4)

    # Creates a folder to store the data of a console
    for console in console_list:
        console_data = Path(hashes + console.lower())
        console_data.mkdir(exist_ok = True)

add_missing_data()

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

# Run the program
if __name__ == '__main__':
    eel.start('index.html', host='localhost', port='5600', size=(1500, 1080))