# Imports
import paths, json, hashlib, re
from switch.switch_game_reader import getTitleID
from pathlib import Path

# Various file name extensions
three_ds_types        = ['3ds', 'cia', 'cxi']
ds_types              = ['nds', 'srl']
gameboy_types         = ['gb']
gameboy_advance_types = ['gba']
gamecube_types        = ['iso', 'gcm', 'gcz', 'rvz']
nes_types             = ['nes', 'prg', 'chr']
nintendo_64_types     = ['n64', 'v64', 'z64']
playstation_types     = ['iso', 'bin']
playstation_2_types   = ['iso', 'bin']
sega_genesis_types    = ['md', 'gen', 'bin']
snes_types            = ['sfc', 'smc', 'fig', 'swc']
switch_types          = ['nsp', 'xci']
wii_types             = ['iso', 'rvz', 'gcz', 'wbfs', 'nkit']
wii_u_types           = ['wud', 'wux']
xbox_types            = ['iso', 'xiso']
xbox_360_types        = ['iso', 'xex']

# Takes the types from above that require grabbing a serial, rather than hashing
serial_types = []

for ext in gamecube_types:
    serial_types.append(ext)

for ext in playstation_types:
    serial_types.append(ext)

for ext in playstation_2_types:
    serial_types.append(ext)

for ext in wii_types:
    serial_types.append(ext)

for ext in xbox_types:
    serial_types.append(ext)

for ext in xbox_360_types:
    serial_types.append(ext)

# Hashes the rom file
def get_hash(rom):
    with open(rom, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# For iso files, this takes the serial of the file instead of hashing it
def get_serials(rom):
    serials = {}

    # Nintendo serial reading
    with open(rom, 'rb') as f:
        nintendo_serial = f.read(6)
        nintendo_serial = nintendo_serial.decode('ascii')

        serials['nintendo'] = nintendo_serial

    # Playstation serial reading
    with open(rom, 'rb') as f:
        playstation_serial = f.read(2 * 1024 * 1024)

    playstation_match = re.search(rb'(S[L|C|U|E|P|M][U|L|S|E|C|D|P|M]-?\d{4,5})', playstation_serial)

    if playstation_match:
        playstation_serial = playstation_match.group(1).decode('utf-8')
        serials['playstation'] = playstation_serial

    # Original Xbox serial reading
    def xbox_serial(type):
        with open(rom, 'rb') as f:
            xbox_serial = f.read(2 * 1024 * 1024)

        # The original does AA-123 but the 360 does AA-1234
        if (type == 'xbox'):
            xbox_match = re.search(rb'([A-Z]{2}-\d{3})', xbox_serial)
        elif (type == 'xbox-360'):
            xbox_match = re.search(rb'([A-Z]{2}-\d{4})', xbox_serial)

        if xbox_match:
            xbox_serial = xbox_match.group(1).decode('utf-8')
            return xbox_serial

    serials['xbox'] = xbox_serial('xbox')
    serials['xbox-360'] = xbox_serial('xbox-360')    

    return serials

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

# Removes file name extensions. Different statements account for .ext vs .exxt for example
def remove_extension_unicode(name):

    # 2 letter extensions
    if name[-3] == '.':
        name = name.replace(name[-3], '')

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
def add_to_storage(rom, name, console, type):
    name = remove_extension_unicode(name)
    display_name = remove_name_filler(name)

    if (console == 'switch') or (console == 'xbox-360'):
        name = remove_name_filler(name)

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        # Changes where it is stored in the file
        if (type == 'hash'):
            data['hashed-roms'][rom] = {'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}{console}/hover/{name}.png'
                                       }
        elif (type == 'serial'):
            data['rom-serials'][rom] = {'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}{console}/hover/{name}.png'
                                       }
            
            # The Xbox 360 database lacks a screenshot image
            if console == 'xbox-360':
                data['rom-serials'][rom]['hover'] = data['rom-serials'][rom]['cover']

    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)

# Switch games are stored differently
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
def check_hash(hash, console):
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
                add_to_storage(hash, current_name, console, 'hash')

# Compares the serial of the rom against the data, and takes the serial and name of the file
def check_serial(serials, console):
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
                        for serial_type in serials:
                            if serials[serial_type] == serial_to_check:
                                add_to_storage(serial_to_check, current_name, console, 'serial')



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
def load_rom_files():
    global roms

    roms_location = Path(paths.roms_path)
    roms = ['roms/' + r.name for r in roms_location.iterdir() if r.is_file()]

load_rom_files()

# Reads through roms and figures out what they are based on extension
def rom_analysis():
    for rom in roms:
        # This is under a condition because hashing large ISOs takes a long time and is useless   
        if rom[-3:] in serial_types:
            serials = get_serials(rom)
            already_found = check_existence(serials)

        # Switch games are special and go through a much different process
        elif rom[-3:] in switch_types:
            already_found = check_existence(rom)

        # This is under a condition because looking for a serial in non-ISOs often causes an error
        else:
            hash = get_hash(rom)
            already_found = check_existence(hash)
            
        if (not already_found):
            if rom[-3:] in three_ds_types:
                check_hash(hash, '3ds')

            if rom[-3:] in ds_types:
                check_hash(hash, 'ds')

            if rom[-2:] in gameboy_types:
                check_hash(hash, 'gb')

            if rom[-3:] in gameboy_types:
                check_hash(hash, 'gba')

            if rom[-3:] in gamecube_types:
                check_serial(serials, 'gamecube')

            if rom[-3:] in nes_types:
                check_hash(hash, 'nes')

            if rom[-3:] in nintendo_64_types:
                check_hash(hash, 'nintendo-64')

            if rom[-3:] in playstation_types:
                check_serial(serials, 'playstation')

            if rom[-3:] in playstation_2_types:
                check_serial(serials, 'playstation-2')

            if (rom[-2:] in sega_genesis_types) or (rom[-3:] in sega_genesis_types):
                check_hash(hash, 'sega-genesis')

            if rom[-3:] in snes_types:
                check_hash(hash, 'snes')

            if rom[-3:] in switch_types:
                title_id = getTitleID(rom, paths.hactool_path, paths.prod_keys_path)
                
                title = check_title_id(title_id)
                
                if title:
                    add_to_switch_storage(rom, title_id, title)

            if (rom[-3:] in wii_types) or (rom[-4:] in wii_types):
                check_serial(serials, 'wii')

            if rom[-3:] in wii_u_types:
                check_serial(serials, 'wii-u')

            if (rom[-3:] in xbox_types) or (rom[-4:] in xbox_types):
                check_serial(serials, 'xbox')

            if rom[-3:] in xbox_360_types:
                check_serial(serials, 'xbox-360')

rom_analysis()