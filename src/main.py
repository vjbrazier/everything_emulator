# Imports
import eel, json, consoles, games
from pathlib import Path

# Initialize
eel.init('web')

# List of consoles
consoles = ['xbox', 'xbox-360', 'gameboy', 'gameboy-advance', 'gamecube', 'DS', '3DS', 'nintendo-64', 'NES', 'SNES', 'wii', 'wii-U', 'switch', 'sega-genesis', 'playstation', 'playstation-2']

# Paths
paths_json = 'data/paths.json'
hashes = 'data/rom-info/'

# Initializes missing data in the paths file
def add_missing_data():
    with open(paths_json, 'r') as f:
        data = json.load(f)

        console_paths = list(data['emulator-paths'].keys())

        for console in consoles:
            if console not in console_paths:
                data['emulator-paths'][console] = ''

        with open(paths_json, 'w') as f:
            json.dump(data, f, indent=4)

    for console in consoles:
        console_data = Path(hashes + console)
        console_data.mkdir(exist_ok = True)

# List of games
games = []

# Dummy data
for i in range(25):
    games.append(f'Game {i}')

# Passes consoles
@eel.expose
def get_consoles():
    return consoles

@eel.expose
def get_games():
    return games

# Run the program
if __name__ == '__main__':
    eel.start('index.html', host='localhost', port='5600', size=(1500, 1080))