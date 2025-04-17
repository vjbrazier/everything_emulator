# Imports
import paths
import json
import hashlib
import re
import eel
import time
import rom_entry
from switch.switch_game_reader import getTitleID
from pathlib import Path

# Various file name extensions
console_extensions = {
    'hash': {
        '3ds':             ['3ds', 'cia', 'cxi'],
        'ds' :             ['nds', 'srl'],
        'gameboy':         ['gb'],
        'gameboy-advance': ['gba'],
        'nes' :            ['nes', 'prg', 'chr'],
        'nintendo-64':     ['n64', 'v64', 'z64'],
        'snes':            ['sfc', 'smc', 'fig', 'swc'],
    },
    'switch':          ['nsp', 'xci'],
    'wii':             ['iso', 'rvz', 'gcz', 'wbfs', 'nkit'],
    'xbox':            ['iso', 'xiso'],
    'xbox-360':        ['iso', 'xex']
}

three_ds_types        = ['3ds', 'cia', 'cxi']
ds_types              = ['nds', 'srl']
gameboy_types         = ['gb']
gameboy_advance_types = ['gba']
gamecube_types        = ['iso', 'gcm', 'gcz', 'rvz']
nes_types             = ['nes', 'prg', 'chr']
nintendo_64_types     = ['n64', 'v64', 'z64']
snes_types            = ['sfc', 'smc', 'fig', 'swc']
switch_types          = ['nsp', 'xci']
wii_types             = ['iso', 'rvz', 'gcz', 'wbfs', 'nkit']
xbox_types            = ['iso', 'xiso']
xbox_360_types        = ['iso', 'xex']

# Takes the types from above that require hashing
hash_types = []

def add_to_cumulative(list):
    for ext in list:
        hash_types.append(ext)

add_to_cumulative(three_ds_types)
add_to_cumulative(ds_types)
add_to_cumulative(gameboy_types)
add_to_cumulative(gameboy_advance_types)
add_to_cumulative(nes_types)
add_to_cumulative(nintendo_64_types)
add_to_cumulative(snes_types)

# Hashes the rom file
def get_hash(rom):
    with open(rom, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# For Wii/Gamecube files, this takes the serial of the file instead of hashing it
def get_serial(rom):
    with open(rom, 'rb') as f:
        serial = f.read(6) #The serial is just the first 6 digits
        serial = serial.decode('ascii')

        return serial

# Removes extra content in the rom name (such as (USA)) that users don't care for
def remove_name_filler(name):
    # List of unwanted region/language tags
    filler_data = [
        'En', 'Fr', 'Es', 'It', 'Js', 'De',
        'Europe', 'Japan', '(World)', 'Asia', 'Australia', 'USA'
    ]

    # Step 1: Remove filler items from grouped language/region lists like (En,Fr,De)
    def clean_lang_group(match):
        items = [i.strip() for i in match.group(1).split(',')]
        kept = [i for i in items if i not in filler_data]
        return f"({', '.join(kept)})" if kept else ''

    name = re.sub(r'\(([^)]+)\)', clean_lang_group, name)

    # Step 2: Remove any remaining standalone filler tokens with common separators
    pattern = r'(\s*[\(\[\-_]?\b(?:' + '|'.join(re.escape(item) for item in filler_data if item != 'USA') + r')\b[\)\]_]*\s*)'
    name = re.sub(pattern, ' ', name, flags=re.IGNORECASE)

    # Step 3: Remove empty parentheses, brackets, dashes, or stray commas
    name = re.sub(r'[\(\[\{][\s,]*[\)\]\}]', '', name)      # Empty ()
    name = re.sub(r'\s{2,}', ' ', name)                     # Extra spaces
    name = re.sub(r'[\s,\-]+$', '', name)                   # Trailing commas/dashes
    name = name.strip()

    return name.replace('(World)', '').strip()

# Removes file name extensions and unicode
def remove_extension_unicode(name):
    # 2 letter extensions
    if name[-3] == '.':
        name = name.replace(name[-3:], '')

    # 3 letter extensions
    elif name[-4] == '.':
        name = name.replace(name[-4:], '')

    # 4 letter extensions
    elif name[-5] == '.':
        name = name.replace(name[-5:], '')

    name = name.replace('\u00ae', '') # Registered Trademark
    name = name.replace('\u2122', '') # Trademark
    name = name.replace('\u00a9', '') # Copyright

    return name.strip()

# Stores your ROMs to eliminate the need to identify them each time
def add_to_storage(rom, rom_identifier, name, console, rom_data):
    name = remove_extension_unicode(name)
    display_name = remove_name_filler(name)

    # The Switch and Xbox-360 image archives lack such data in their names
    if (console == 'switch') or (console == 'xbox-360'):
        name = display_name

    rom_data[rom] = {'rom-identifier': rom_identifier,
                 'name': name,
                 'display-name': display_name,
                 'console': console,
                 'cover-image': f'{paths.rom_info_path}{console}/cover/{name}.png',
                 'hover-image': f'{paths.rom_info_path}{console}/hover/{name}.png',
                }
    
    # The Switch and Xbox-360 image archives lack a hover-image
    if (console == 'switch') or (console == 'xbox-360'):
        rom_data[rom]['hover-image'] = rom_data[rom]['cover-image']

# Compares the hash of the rom against the data, and takes the hash and name of the file
def check_hash(rom, hash, rom_data, console):
    console_file = console + '.dat'

    with open(paths.rom_info_path + console + '/' + console_file, 'r', encoding = 'utf-8') as f:
        for line in f:
            hash_to_check = re.search(r'md5\s+([0-9A-Fa-f]{32})', line)
            current_name = re.search(r'name\s+"(.+?)"', line)

            # These two checks prevent an error from accessing the group of a None object
            if hash_to_check:
                hash_to_check = hash_to_check.group(1).lower()
            
            if current_name:
                current_name = current_name.group(1)
            
            if hash == hash_to_check:
                add_to_storage(rom, hash, current_name, console, rom_data)
                return True

# Compares the serial of the rom against the data, and takes the serial and name of the file
def check_serial(rom, serial, rom_data, console):
    console_file = console + '.dat'

    with open(paths.rom_info_path + console + '/' + console_file, 'r', encoding='utf-8') as f:
        inside_game_block = False
        current_name = None

        for line in f:
            line = line.strip()

            if line.startswith('game ('):
                inside_game_block = True
                current_name = None  # Reset the game name for each new block

            if inside_game_block:
                if current_name is None:
                    match = re.search(r'name\s+"(.+?)"', line)
                    if match:
                        current_name = match.group(1)

                # Look for a serial
                serial_match = re.search(r'serial\s+"([A-Z0-9]{6})"', line)
                if serial_match:
                    serial_to_check = serial_match.group(1)

                    # Check for a match only if current_name is set
                    if current_name:
                        if serial == serial_to_check:
                            add_to_storage(rom, serial_to_check, current_name, console, rom_data)
                            return True

def check_title_id(title_id):
    with open(paths.rom_info_path + 'switch/switch.json', 'r') as f:
        data = json.load(f)

        for id in list(data.keys()):
            if data[id]['id'] == title_id:
                return data[id]['name']

# Checks if a hash is already stored prior to searching the entire database again
def check_existence(rom, data):
    return data.get(rom, '') != ''

# Creates a list of all the roms stored
@eel.expose
def load_rom_files():
    # Handles the directory being empty
    if paths.roms_path == '':
        return []
    
    # ext = Path(rom).suffix.lower().lstrip('.')

    roms_location = Path(paths.roms_path)
    roms = [paths.roms_path + r.name for r in roms_location.iterdir() if r.is_file()]

    return roms

# Creates a list of ROMs not already stored
@eel.expose
def load_new_rom_files():
    roms = load_rom_files()

    # Reopens due to being called by the JS
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

    return [rom for rom in roms if not check_existence(rom, data)]

# Counts how many new files exist for the loading page
@eel.expose
def count_new_roms():
    roms = load_rom_files()

    # Reopens due to being called by the JS
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

    return sum(1 for rom in roms if not check_existence(rom, data))

# Reads through roms and figures out what they are based on extension
@eel.expose
def rom_analysis():
    unidentified_roms = []
    total = count_new_roms()

    roms = load_rom_files()
    first_time = True

    # Opened at the start and passed around to prevent unnecessary I/O
    with open(paths.rom_data_path, 'r') as f:
        rom_data = json.load(f)

    # Loops through all of the ROMs
    for rom in roms:
        # Does a check to make finding a game you already have unnecessary
        already_found = check_existence(rom, rom_data)
            
        ext = Path(rom).suffix.lower().lstrip('.')

        # Skips the ROM if the ROM has already been stored
        if already_found:
            continue

        # This is set at the start each time. When roms are checked, they return true if found
        # In the event that this remains as None, then it's added to a list for user-input later
        identified_file = None

        eel.update_info(rom, total, first_time)
        time.sleep(1)
        first_time = False


        # This is under a condition to skip Gamecube and Wii games since they require a serial
        if ext in hash_types:
            hash = get_hash(rom)

        if ext in three_ds_types:
            identified_file = check_hash(rom, hash, rom_data, '3ds')

        elif ext in ds_types:
            identified_file = check_hash(rom, hash, rom_data, 'ds')

        elif ext in gameboy_types:
            identified_file = check_hash(rom, hash, rom_data, 'gameboy')

        elif ext in gameboy_advance_types:
            identified_file = check_hash(rom, hash, rom_data, 'gameboy-advance')

        elif ext in nes_types:
            identified_file = check_hash(rom, hash, rom_data, 'nes')

        elif ext in nintendo_64_types:
            identified_file = check_hash(rom, hash, rom_data, 'nintendo-64')

        elif ext in snes_types:
            identified_file = check_hash(rom, hash, rom_data, 'snes')

        # Switch games use a different process
        if ext in switch_types:
            title_id = getTitleID(rom, paths.hactool_path, paths.prod_keys_path)
            
            if title_id:
                title = check_title_id(title_id)
                
            if title:
                identified_file = True
                add_to_storage(rom, title_id, title, 'switch', rom_data)

        # These are ISO files, and have a different process
        if (ext in gamecube_types) or (ext in wii_types):
            # Getting the serial is very fast and easy, so we just get it regardless
            serial = get_serial(rom)

            # Checks the gamecube and wii data first
            identified_file = check_serial(rom, serial, rom_data, 'gamecube')
            
            if (identified_file == None):
                identified_file = check_serial(rom, serial, rom_data, 'wii')

            # Hashing takes longer. If it is neither of the above, then it checks for xbox and xbox 360
            if (identified_file == None):
                hash = get_hash(rom)

                identified_file = check_hash(rom, hash, rom_data, 'xbox')

                if (identified_file == None):
                    identified_file = check_hash(rom, hash, rom_data, 'xbox-360')

        if (identified_file):
            time.sleep(0.5)
            eel.add_rom(rom, True)
        else: 
            time.sleep(0.5)
            eel.add_rom(rom, False)
            unidentified_roms.append(rom)

    # Writes any updated data
    with open(paths.rom_data_path, 'w') as f:
        json.dump(rom_data, f, indent=4)

    # This calls it one last time when finished to make it increment and finish the page
    print(f"Sending update_info: {rom}, first_time: {first_time}")
    time.sleep(1)

    # This would not stop bugging out. I have no idea why, and have gave up. This is the "fix"
    eel.update_info('Complete!', total, first_time)
    eel.update_info('Complete!', total, first_time)
    eel.update_info('Complete!', total, first_time)

    # Only brings up the entry page if needed
    if (unidentified_roms != []):
        rom_entry.initialize(unidentified_roms)