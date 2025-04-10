# Imports
import eel, json, hashlib
from pathlib import Path

# Paths
paths_json = 'data/paths.json'
hashes = 'data/rom-info/'

# Various file name extensions
nintendo_64_types = ['n64', 'v64', 'z64']
snes_types = ['sfc', 'smc', 'fig', 'swc']

def hash_rom(file, hash_type):
    hasher = hashlib.new(hash_type)

    with open(file, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)

    return(hasher.hexdigest)


with open(paths_json, 'r') as f:
    data = json.load(f)

    roms_location = Path('roms')
    roms = ['roms/' + r.name for r in roms_location.iterdir() if r.is_file()]

    print(roms)

for rom in roms:
    hash = hash_rom(rom, 'md5')

    if rom[-3:] in nintendo_64_types:
        print('hi')

    elif rom[-3:] in snes_types:
        print('hi')