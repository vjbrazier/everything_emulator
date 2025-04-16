import paths, eel, json, os, tkinter as tk, shutil
from tkinter import filedialog

hash_types = ['3ds', 'ds', 'gameboy', 'gameboy-advance', 'nes', 'nintendo-64', 'snes', 'xbox', 'xbox-360']

def initialize(unidentified_roms):
    global roms
    global current_index

    eel.show('rom_entry.html')

    roms = unidentified_roms
    current_index = 0

@eel.expose
def page_ready():
    global roms

    eel.next_entry(roms[0])()

@eel.expose
def cycle_rom():
    global current_index
    global roms

    current_index += 1
    
    if (current_index == len(roms)):
        eel.close_window()
    else:
        eel.next_entry(roms[current_index])

@eel.expose
def pick_image(subfolder):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_path = filedialog.askopenfilename(parent = root, title = 'Select the image desired')
    root.destroy()

    if (file_path != ''):
        if (subfolder == 'cover'):
            shutil.copy(file_path, paths.temp_cover_path)
            return paths.temp_cover_path[4:] # Removes web/

        elif (subfolder =='hover'):
            shutil.copy(file_path, paths.temp_hover_path)
            return paths.temp_hover_path[4:] # Removes web/
        
# The website name will always be http://url/*. This removes that prefix to get the file location
def get_file_location(path):
    index = path.find('//')
    index = path.find('/', index + 2)
    return path[index+1:]

@eel.expose
def create_data(rom, name, console, cover, hover):
    new_cover_path = paths.rom_info_path + console + '/cover/'
    new_hover_path = paths.rom_info_path + console + '/hover/'
    
    cover = get_file_location(cover)
    shutil.copy('web/' + cover, new_cover_path + 'cover.png')

    if (os.path.exists(new_cover_path + name + '.png')):
        os.remove(new_cover_path + name + '.png')

    os.rename(new_cover_path + 'cover.png', new_cover_path + name + '.png')
    cover = new_cover_path + name + '.png'

    hover = get_file_location(hover)
    shutil.copy('web/' + hover, new_hover_path + 'hover.png')

    if (os.path.exists(new_hover_path + name + '.png')):
        os.remove(new_hover_path + name + '.png')

    os.rename(new_hover_path + 'hover.png', new_hover_path + name + '.png')
    hover = new_hover_path + name + '.png'

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

        if console in hash_types:
            category = 'hashed-roms'
        elif console == 'switch':
            category = 'switch-games'
        else:
            category = 'rom-serials'

        rom = 'roms/' + rom

        data[category][rom] = {}
        data[category][rom] = {'display-name': name, 'console': console, 'cover': cover, 'hover': hover}

    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)