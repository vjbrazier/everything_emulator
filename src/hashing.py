# Imports
import paths, json, hashlib, re
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
def hash_rom(file):
    with open(file, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# For iso files, this takes the serial of the file instead of hashing it
def get_serial(file):
    with open(file, 'rb') as f:
        serial = f.read(6)
        serial = serial.decode('ascii')

        return serial

# Removes extra content in the rom name (such as (USA)) that users don't care for
def remove_name_filler(name):
    filler_data = [
                   'En', 'Fr', 'Es', 'It', 'Js', 'De',
                   'USA', 'Europe', 'Japan', 'World',
                   '()',
                  ]

    for data in filler_data:
        name = name.replace(data, '')

    return name.strip()

# Removes file name extensions. Different statements account for .ext vs .exxt for example
def remove_extension(name):
    if name[-4] == '.':
        name = name.replace(name[-4:], '')
    elif name[-5] == '.':
        name = name.replace(name[-5:], '')

    return name.strip()

# When a match is found from hashing/serialling, it stores it in the file
# This makes it so all of your roms don't need to be rehashed and searched for prior to loading again
def add_to_storage(rom, name, console, type):
    name = remove_extension(name)
    display_name = remove_name_filler(name)

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        # Changes where it is stored in the file
        if (type == 'hash'):
            data['hashed-roms'][rom] = {'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}/{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}/{console}/hover/{name}.png'
                                       }
        elif (type == 'serial'):
            data['rom-serials'][rom] = {'name': name, 'display-name': display_name, 'console': console,
                                        'cover': f'{paths.rom_info_path}{console}/cover/{name}.png',
                                        'hover': f'{paths.rom_info_path}{console}/hover/{name}.png'
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
def check_serial(serial, console):
    console_file = console + '.dat'

    with open(paths.rom_info_path + console + '/' + console_file, 'r', encoding = 'utf-8') as f:
        # Due to the way the file is setup, we need this extra boolean
        inside_game_block = False

        for line in f:
            line = line.strip()

            # Ensures we are in the right spot, and resets the name prior to getting a value for it
            if (line.startswith('game (')):
                inside_game_block = True
                current_name = None

            if inside_game_block and not current_name:
                current_name = re.search(r'name\s+"(.+?)"', line)
                
                # A quick check to ensure we don't call group on a None object
                if current_name:
                    current_name = current_name.group(1)


            serial_to_check = re.search(r'serial\s+"([A-Z0-9]{6})"', line)

            # Another check for above
            if serial_to_check:
                serial_to_check = serial_to_check.group(1)
                
            if serial == serial_to_check:
                add_to_storage(serial, current_name, console, 'serial')

# Checks if a hash is already stored prior to searching the entire database again
def check_existence(rom):
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        if (rom in list(data['hashed-roms'].keys())) or (rom in list(data['rom-serials'].keys())):
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
            serial = get_serial(rom)
            already_found = check_existence(serial)

        # This is under a condition because looking for a serial in non-ISOs often causes an error
        else:
            hash = hash_rom(rom)
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
                check_serial(serial, 'gamecube')

            if rom[-3:] in nes_types:
                check_hash(hash, 'nes')

            if rom[-3:] in nintendo_64_types:
                check_hash(hash, 'nintendo-64')

            if rom[-3:] in playstation_types:
                check_serial(serial, 'playstation')

            if rom[-3:] in playstation_2_types:
                check_serial(serial, 'playstation-2')

            if (rom[-2:] in sega_genesis_types) or (rom[-3:] in sega_genesis_types):
                check_hash(hash, 'sega-genesis')

            if rom[-3:] in snes_types:
                check_hash(hash, 'snes')

            if rom[-3:] in switch_types:
                pass

            if (rom[-3:] in wii_types) or (rom[-4:] in wii_types):
                check_serial(serial, 'wii')

            if rom[-3:] in wii_u_types:
                check_serial(serial, 'wii-u')

            if (rom[-3:] in xbox_types) or (rom[-4:] in xbox_types):
                pass

            if rom[-3:] in xbox_360_types:
                pass

rom_analysis()