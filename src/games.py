# Imports
import paths
import eel
import json
import hashing
import time
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from custom_logger import add_to_log

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
    eel.show('web/loading.html')
    time.sleep(1) # Similar to above
    eel.close_main_window()

# Opens the file explorer for the user to select the rom folder
@eel.expose
def modify_rom_path():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_path = filedialog.askdirectory(parent = root, title = 'Select the rom folder')

    try:
        update_rom_path(file_path)
    except Exception:
        add_to_log("[WARN] You didn't seem to choose a folder.")

    root.destroy()

# Loads games that have been logged in the data
@eel.expose
def get_game_data():
    # List of games
    with open(paths.rom_data_path, 'r') as f:
        game_data = json.load(f)

    return game_data

# Deletes an entry upon click
@eel.expose
def delete_entry(entry):
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

    try:
        del data[entry]
        add_to_log(f'[INFO] Deleted entry {entry}')
    except Exception as e:
        add_to_log(f'[ERROR] Attempted to delete {entry}, received {e}')

    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)

    eel.reload_main_window()

# Starts a game
@eel.expose
def start_game(game, console):
    with open(paths.file_paths, 'r') as f:
        data = json.load(f)

    console_path = data['emulator-paths'].get(console)

    if not console_path:
        
        add_to_log(f"[ERROR] You don't have an emulator setup for {console}")
        eel.game_open_error("[ERROR] You don't have an emulator setup for ", console)
        return

    try:
        if (not os.path.exists(game)):
            error = f'[ERROR] Game not found: {game[game.rfind('/') + 1:]}'

            eel.game_open_error(error, '')
            raise FileNotFoundError(error)
        
        if (not os.path.exists(console_path)):
            error = f'[ERROR] Emulator not found: {console_path}'

            eel.game_open_error(error, '')
            raise FileNotFoundError(error)
        
        subprocess.Popen([console_path, game])
        add_to_log(f'[INFO] Opened {game} with {console_path}')
        
    except Exception as e:
        error = f'[ERROR] Failure: {e}'
        
        eel.game_open_error(error, '')
        print(error)
