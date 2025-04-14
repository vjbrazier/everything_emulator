# Imports
import paths, json, hashlib, re, eel
from switch.switch_game_reader import getTitleID
from pathlib import Path
from datetime import datetime

# Various file name extensions
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

# When a match is found from hashing/serialling, it stores it in the file
# This makes it so all of your roms don't need to be rehashed and searched for prior to loading again
def add_to_storage(rom, rom_identifier, name, console, type):
    name = remove_extension_unicode(name)
    display_name = remove_name_filler(name)

    # The image archive for the Xbox-360 does not contain the extra info
    if console == 'xbox-360':
        name = remove_name_filler(name)

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        # Changes where it is stored in the file
        if (type == 'hash'):
            data['hashed-roms'][rom] = {'hash': rom_identifier,
                                        'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}{console}/hover/{name}.png'
                                       }
            
            # The Xbox 360 database lacks a screenshot image
            if console == 'xbox-360':
                data['rom-serials'][rom]['hover'] = data['rom-serials'][rom]['cover']

        elif (type == 'serial'):
            data['rom-serials'][rom] = {'serial': rom_identifier,
                                        'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}{console}/hover/{name}.png'
                                       }

    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)

# Switch games are stored with some different data
def add_to_switch_storage(rom, title_id, title):
    title = remove_extension_unicode(title)
    display_name = remove_name_filler(title)

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        # The switch database lacks a screenshot image
        data['switch-games'][rom] = {'title-id': title_id, 'console': 'switch', 'display-name': display_name,
                                     'cover': f'{paths.rom_info_path}switch/cover/{title}.png',
                                     'hover': f'{paths.rom_info_path}switch/cover/{title}.png'
                                    }
        
    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)

# Compares the hash of the rom against the data, and takes the hash and name of the file
def check_hash(rom, hash, console):
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
                add_to_storage(rom, hash, current_name, console, 'hash')

# Compares the serial of the rom against the data, and takes the serial and name of the file
def check_serial(rom, serial, console):
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
                            add_to_storage(rom, serial_to_check, current_name, console, 'serial')
                            return True
    return False

def check_title_id(title_id):
    with open(paths.rom_info_path + 'switch/switch.json', 'r') as f:
        data = json.load(f)

        for id in list(data.keys()):
            if data[id]['id'] == title_id:
                return data[id]['name']

# Checks if a hash is already stored prior to searching the entire database again
def check_existence(rom):
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        hashed_roms  = list(data['hashed-roms'].keys())
        rom_serials  = list(data['rom-serials'].keys())
        switch_games = list(data['switch-games'].keys())

        if (rom in hashed_roms) or (rom in rom_serials) or (rom in switch_games):
            return True
        else:
            return False

# Creates a list of all the roms stored
@eel.expose
def load_rom_files():
    global roms

    roms_location = Path(paths.roms_path)
    roms = ['roms/' + r.name for r in roms_location.iterdir() if r.is_file()]

    return roms

# Reads through roms and figures out what they are based on extension
def rom_analysis():
    for rom in roms:
        # Does a check to make finding a game you already have unnecessary
        already_found = check_existence(rom)
            
        if (not already_found):
            # This is under a condition to skip Wii games since they require a serial
            if rom[-3:] in hash_types:
                hash = get_hash(rom)
            
            if rom[-3:] in three_ds_types:
                check_hash(rom, hash, '3ds')

            if rom[-3:] in ds_types:
                check_hash(rom, hash, 'ds')

            if rom[-2:] in gameboy_types:
                check_hash(rom, hash, 'gameboy')

            if rom[-3:] in gameboy_types:
                check_hash(rom, hash, 'gameboy-advance')

            if rom[-3:] in nes_types:
                check_hash(rom, hash, 'nes')

            if rom[-3:] in nintendo_64_types:
                check_hash(rom, hash, 'nintendo-64')

            if rom[-3:] in snes_types:
                check_hash(rom, hash, 'snes')

            # Switch games use a different process
            if rom[-3:] in switch_types:
                title_id = getTitleID(rom, paths.hactool_path, paths.prod_keys_path)
                
                title = check_title_id(title_id)
                
                if title:
                    add_to_switch_storage(rom, title_id, title)

            # These are ISO files, and have a different process
            if (rom[-3:] in gamecube_types) or (rom[-3:] in wii_types) or (rom[-4:] in wii_types):
                # Getting the serial is very fast, so we just get it regardless
                serial = get_serial(rom)

                # Checks the gamecube and wii data first
                game_found = check_serial(rom, serial, 'gamecube')
                
                if (not game_found):
                    game_found = check_serial(rom, serial, 'wii')

                # Hashing takes longer. If it is neither of the above, then it checks for xbox and xbox 360
                if (not game_found):
                    hash = get_hash(rom)
                    check_hash(rom, hash, 'xbox')
                    check_hash(rom, hash, 'xbox-360')
