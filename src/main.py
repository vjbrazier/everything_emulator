# Imports
import paths, eel, json, hashing
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

# Counts how many new files exist for the loading page
@eel.expose
def count_hashing(roms):
    total = 0

    for rom in roms:
        if (not hashing.check_existence(rom)):
            total += 1

    return total

@eel.expose
def begin_hashing(rom):


@eel.expose
def route_to_main():
    # Only imports the elements after its time to have them be active
    import consoles, games

    eel.show('index.html')

# Run the program
if __name__ == '__main__':
    eel.start('loading.html', host='localhost', port='5600', size=(1500, 1080))