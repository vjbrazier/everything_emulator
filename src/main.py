# Import
import eel, os, json, hashlib, tkinter as tk
from tkinter import filedialog

# Initialize
eel.init('web')

# List of consoles
consoles = ['xbox', 'xbox-360', 'gameboy', 'gameboy-advance', 'gamecube', 'ds', '3ds', 'nintendo-64', 'nes', 'snes', 'wii', 'wii-u', 'switch', 'sega-genesis', 'playstation', 'playstation-2']
paths_json = "data/paths.json"

# Initializes missing data in the paths file
with open(paths_json, 'r') as f:
    data = json.load(f)

    console_paths = list(data["emulator-paths"].keys())

    for console in consoles:
        if console not in console_paths:
            data["emulator-paths"][console] = ""

    with open(paths_json, 'w') as f:
        json.dump(data, f, indent=4)

@eel.expose
def check_console_path(console):
    with open(paths_json, 'r') as f:
        data = json.load(f)

        if (data['emulator-paths'][console] == ''):
            return False
        else:
            return True

@eel.expose
def open_console(console):
    with open(paths_json, 'r') as f:
        data = json.load(f)

        if data["emulator-paths"][console] == "":
            return False
        
        else:
            os.startfile(data["emulator-paths"][console])

@eel.expose
def user_console_selection(console):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select the .exe of the emulator")
    update_console(console, file_path)
    root.destroy()

def update_console(console, path):
    with open('paths.json', 'r') as f:
        data = json.load(f)

        data["emulator-paths"][console] = path

    with open('paths.json', 'w') as f:
        json.dump(data, f, indent=4)


# List of games
games = []
# games = ['Super Mario World', 'Mario Odyssey', 'Mario Kart', 'Mario Party', 'Mario 64', 'Mario Galaxy', "Luigi's Mansion"]


# Dummy data
for i in range(25):
    games.append(f"Game {i}")

# Passes consoles
@eel.expose
def get_consoles():
    return consoles

@eel.expose
def get_games():
    return games

# Run the program
if __name__ == '__main__':
    eel.start("index.html", host="localhost", port="5600", size=(1920, 1080))