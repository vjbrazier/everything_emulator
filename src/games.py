# Imports
import eel, json, hashlib, re
from pathlib import Path

# Paths
paths_json = 'data/paths.json'
data_path = 'data/rom-info/'
hashes = 'data/rom-info/'

# Various file name extensions
gameboy_types = ['gb']
gameboy_advance_types = ['gba']
nintendo_64_types = ['n64', 'v64', 'z64']
snes_types = ['sfc', 'smc', 'fig', 'swc']
wii_types = ['iso', 'rvz', 'gcz','wbfs', 'nkit']

# Hashes the rom file. Has two hash types as a backup in case it is needed
def hash_rom(file, hash_type):
    with open(file, 'rb') as f:
        if hash_type == 'md5':
            return hashlib.md5(f.read()).hexdigest()
        elif hash_type == 'sha1':
            return hashlib.sha1(f.read()).hexdigest()
        else:
            print('That seems to be an unsupported hash type')

# For iso files, this takes the serial of the file instead of hashing it
def get_serial(file):
    with open(file, 'rb') as f:
        serial_bytes = f.read(6)
        serial = serial_bytes.decode('ascii')

        return serial

# Removes extra content in the rom name (such as (USA)) that users don't care for
def trim_rom_name(name):
    # Extra stuff included in the title that is not really needed
    filler_data = [
        'En',
        'Fr',
        'Es',
        'It',
        'Js',
        'De',
        'USA',
        'Europe',
        'Japan',
        'World',
        '()',
    ]

    for dat in filler_data:
        if dat in name:
            print(dat)
        name = name.replace(dat, '')

    # Removes file name extensions. Different statements account for .ext vs .exxt for example
    # The reason this is separate from above is to avoid repeating every file extension here
    # Checks at the end so something like Dr. Mario doesn't become Dr Mario
    if name[-4] == '.':
        name = name.replace(name[-4:], '')
    elif name[-5] == '.':
        name = name.replace(name[-5:], '')

    return name.strip()

# When a match is found from hashing/serialling, it stores it in the file
# This makes it so all of your roms don't need to be rehashed and searched for prior to loading again
def add_to_storage(input, name, console, type):
    display_name = trim_rom_name(name)

    with open('data/hashes.json', 'r') as f:
        data = json.load(f)

        if (type == 'hash'):
            data['hashed-roms'][input] = {'name': name, 'display-name': display_name, 'console': console}
        elif (type == 'serial'):
            data['rom-serials'][input] = {'name': name, 'display-name': display_name, 'console': console}

    with open('data/hashes.json', 'w') as f:
        json.dump(data, f, indent=4)

# Compares the hash of the rom against the data, and takes the hash and name of the file
def check_hash(hash, console):
    console_dat = console + '.dat'

    with open(data_path + console + '/' + console_dat, 'r', encoding = 'utf-8') as f:
        for line in f:

            hash_to_check = re.search(r'md5\s+([0-9A-Fa-f]{32})', line)
            current_name = re.search(r'name\s+"(.+?)"', line)

            if hash_to_check:
                hash_to_check = hash_to_check.group(1).lower()

            if current_name:
                current_name = current_name.group(1)
            
            if hash == hash_to_check:
                # print(hash_to_check)
                # print(current_name)
                
                # print('match!')
                add_to_storage(hash, current_name, console, 'hash')

# Compares the serial of the rom against the data, and takes the serial and name of the file
def check_serial(serial, console):
    console_dat = console + '.dat'

    with open(data_path + console + '/' + console_dat, 'r', encoding = 'utf-8') as f:
        inside_game_block = False

        for line in f:
            line = line.strip()

            if (line.startswith('game (')):
                inside_game_block = True
                current_name = None

            if inside_game_block and not current_name:
                current_name = re.search(r'name\s+"(.+?)"', line)
                
                if current_name:
                    current_name = current_name.group(1)
                    # print(current_name)

            serial_to_check = re.search(r'serial\s+"([A-Z0-9]{6})"', line)

            if serial_to_check:
                serial_to_check = serial_to_check.group(1)
                # print(serial_to_check)

            

            if serial == serial_to_check:
                print(serial_to_check)
                print(current_name)
                
                # print('match!')
                add_to_storage(serial, current_name, console, 'serial')

# Checks if a hash is already stored prior to searching the entire database again
def check_existence(input, type):
    with open('data/hashes.json', 'r') as f:
        data = json.load(f)

        if (type == 'hash'):
            if input in list(data['hashed-roms'].keys()):
                print('Already stored')
                return True

            else:
                return False
        elif (type == 'serial'):
            if input in list(data['rom-serials'].keys()):
                print('Already stored')
                return True
            
            else:
                return False

# Loads up all of your roms on start
with open(paths_json, 'r') as f:
    data = json.load(f)

    roms_location = Path('roms')
    roms = ['roms/' + r.name for r in roms_location.iterdir() if r.is_file()]

    print(roms)

for rom in roms:
    
    if (rom[-3:] != 'iso'):
        hash = hash_rom(rom, 'md5')
        print(hash)
        already_found = check_existence(hash, 'hash')

    if (rom[-3:] == 'iso'):
        serial = get_serial(rom)
        print(serial)
        already_found = check_existence(serial, 'serial')
    


    if (not already_found):
        if rom[-2:] in gameboy_types:
            check_hash(hash, 'gb')

        elif rom[-3:] in gameboy_types:
            check_hash(hash, 'gba')

        elif rom[-3:] in nintendo_64_types:
            # print(f'{hash}: n64')
            check_hash(hash, 'nintendo-64')

        elif rom[-3:] in snes_types:
            # print(f'{hash}: snes')
            check_hash(hash, 'snes')

        elif (rom[-3:] in wii_types) or (rom[-4:] in wii_types):
            check_serial(serial, 'wii')