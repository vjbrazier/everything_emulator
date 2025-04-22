import paths
import eel
import json
import os
import shutil
import tkinter as tk
from custom_logger import add_to_log
from tkinter import filedialog
from urllib.parse import quote

def initialize(unidentified_roms, roms_missing_data):
    global roms
    global missing_roms
    global current_index

    eel.show('web/rom_entry.html')

    roms = unidentified_roms
    missing_roms = roms_missing_data
    current_index = 0

@eel.expose
def entry_page_ready():
    global roms
    global missing_roms

    add_to_log('[INFO] Entry Page is ready!')

    if (roms != []):
        add_to_log('[INFO] Setting up unidentified ROM menu')
        eel.next_unidentified_entry(roms[0])
    else:
        data = find_existing_data(missing_roms[0])

        rom_name     = data.get('display-name')
        rom_console  = data.get('console')
        rom_py_cover = data.get('py-cover-image')
        rom_js_cover = data.get('js-cover-image')
        rom_py_hover = data.get('py-hover-image')
        rom_js_hover = data.get('js-hover-image')

        add_to_log(f'[INFO] Setting up missing data ROM menu, using {rom_name}, {rom_console}, {rom_py_cover}, {rom_js_cover}, {rom_py_hover}, and {rom_js_hover}')
        eel.next_missing_entry(missing_roms[0], rom_name, rom_console, rom_py_cover, rom_js_cover, rom_py_hover, rom_js_hover)

# Finds what data is and is not missing (just images)
def find_existing_data(rom):
    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

    data = data.get(rom)

    existing_data = {}
    existing_data['display-name'] = data.get('display-name')
    existing_data['console'] = data.get('console')
    
    if (os.path.exists(data.get('py-cover-image'))):
        add_to_log(f'[INFO] Cover image found for {rom}')
        existing_data['py-cover-image'] = data.get('py-cover-image')
        existing_data['js-cover-image'] = '../' + data.get('js-cover-image')

    else:
        existing_data['py-cover-image'] = ''
        existing_data['js-cover-image'] = 'images/placeholder.svg'

    if (os.path.exists(data.get('py-hover-image'))):
        add_to_log(f'[INFO] Hover image found for {rom}')
        existing_data['py-hover-image'] = data.get('py-hover-image')
        existing_data['js-hover-image'] = '../' + data.get('js-hover-image')

    else:
        existing_data['py-hover-image'] = ''
        existing_data['js-hover-image'] = 'images/placeholder.svg'

    return existing_data

@eel.expose
def cycle_unidentified_roms():
    global current_index
    global roms
    global missing_roms

    current_index += 1
    
    if (current_index >= len(roms)):
        if missing_roms != []:
            current_index = 0

            data = find_existing_data(missing_roms[0])

            rom_name     = data.get('display-name')
            rom_console  = data.get('console')
            rom_py_cover = data.get('py-cover-image')
            rom_js_cover = data.get('js-cover-image')
            rom_py_hover = data.get('py-hover-image')
            rom_js_hover = data.get('js-hover-image')

            add_to_log(f'[INFO] Setting up missing data ROM menu, using {rom_name}, {rom_console}, {rom_py_cover}, {rom_js_cover}, {rom_py_hover}, and {rom_js_hover}')
            eel.next_missing_entry(missing_roms[0], rom_name, rom_console, rom_py_cover, rom_js_cover, rom_py_hover, rom_js_hover)
        else:
            eel.close_entry_window()
            eel.reload_main_window()
    else:
        eel.next_unidentified_entry(roms[current_index])


@eel.expose
def cycle_missing_roms():
    global current_index
    global missing_roms

    current_index += 1

    if (current_index >= len(missing_roms)):
        eel.close_entry_window()
        eel.reload_main_window()
    else:
        data = find_existing_data(missing_roms[current_index])

        rom_name     = data.get('display-name')
        rom_console  = data.get('console')
        rom_py_cover = data.get('py-cover-image')
        rom_js_cover = data.get('js-cover-image')
        rom_py_hover = data.get('py-hover-image')
        rom_js_hover = data.get('js-hover-image')

        add_to_log(f'[INFO] Setting up missing data ROM menu, using {rom_name}, {rom_console}, {rom_py_cover}, {rom_js_cover}, {rom_py_hover}, and {rom_js_hover}')
        eel.next_missing_entry(missing_roms[current_index], rom_name, rom_console, rom_py_cover, rom_js_cover, rom_py_hover, rom_js_hover)

@eel.expose
def pick_image(subfolder):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_path = filedialog.askopenfilename(parent = root, title = 'Select the image desired')
    root.destroy()

    if not file_path:
        return

    if (subfolder == 'cover'):
        shutil.copy(file_path, paths.temp_cover_path)
        return paths.temp_cover_path[4:] # Removes web/, as JS doesn't need it
    
    elif (subfolder =='hover'):
        shutil.copy(file_path, paths.temp_hover_path)
        return paths.temp_hover_path[4:] # Removes web/, as JS doesn't need it
        
@eel.expose
def copy_cover_to_hover():
    shutil.copy(paths.temp_cover_path, paths.temp_hover_path)
    return paths.temp_hover_path

# The website name will always be http://url/*. This removes that prefix to get the file location
def get_file_location(path):
    index = path.find('//')

    if (index == -1):
        return path
    
    index = path.find('/', index + 2)
    return path[index+1:]

def setup_images(image_path, name, new_path, type):
    add_to_log(f'[INFO] Setting up images with setup_images()! Using {image_path}, {name}, {new_path}, and {type}')
    
    # Prevents a duplicate
    image_path = image_path.lstrip('web/')

    shutil.copy(f'web/{image_path}', f'{new_path}{type}.png')

    if (os.path.exists(f'{new_path}{name}.png')):
        os.remove(f'{new_path}{name}.png')

    os.rename(f'{new_path}{type}.png', f'{new_path}{name}.png')

    return f'{new_path}{name}.png'

@eel.expose
def create_data(rom, name, console, py_cover, py_hover, backup_cover, backup_hover):
    add_to_log(f'[INFO] Creating data with create_data()! Using {rom}, {name}, {console}, {py_cover}, {py_hover}, {backup_cover}, {backup_hover}')

    new_cover_path = paths.rom_info_path + console + '/cover/'
    new_hover_path = paths.rom_info_path + console + '/hover/'
    
    # When submitting missing data, these covers come back encoded for JS
    # The backup parameters only have data if calling from missing, hence the condition
    if '%' not in py_cover:
        py_cover_location = get_file_location(py_cover)
        py_cover = setup_images(py_cover_location, name, new_cover_path, 'cover')
        js_cover = '../' + new_cover_path + quote(name) + '.png'

    else:
        py_cover = backup_cover
        temp_name = py_cover[py_cover.rfind('/') + 1:]
        js_cover = '../' + new_cover_path + quote(temp_name)

    if '%' not in py_hover:
        py_hover_location = get_file_location(py_hover)
        py_hover = setup_images(py_hover_location, name, new_hover_path, 'hover')
        js_hover = '../' + new_hover_path + quote(name) + '.png'
        
    else:
        py_hover = backup_hover
        temp_name = py_hover[py_hover.rfind('/') + 1:]
        js_hover = '../' + new_hover_path + quote(temp_name)

    with open(paths.rom_data_path, 'r') as f:
        data = json.load(f)

    # Although some of this data is repeated, it is here for consistency
    data[rom] = {'rom-identifier': rom,
                 'name': name, 
                 'display-name': name,
                 'console': console, 
                 'py-cover-image': py_cover, 
                 'js-cover-image': js_cover,
                 'py-hover-image': py_hover,
                 'js-hover-image': js_hover
                }

    with open(paths.rom_data_path, 'w') as f:
        json.dump(data, f, indent=4)