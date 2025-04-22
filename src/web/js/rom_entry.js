// Images
const cover = document.getElementById('cover');
const cover_preview = document.getElementById('cover-preview');
const hover = document.getElementById('hover');
const hover_preview = document.getElementById('hover-preview');

cover.addEventListener('click', async function () {
    const file = await eel.pick_image('cover')();

    if (file) {
        cover_preview.src = file;
    } else {
        cover_preview.src = 'images/placeholder.svg';
    }
})

hover.addEventListener('click', async function () {
    const file = await eel.pick_image('hover')();

    if (file) {
        hover_preview.src = file;
    } else {
        hover_preview.src = 'images/placeholder.svg';
        console.log(hover_preview.src);
    }
})

function getFileLocation(path) {
    let index = path.indexOf('//');

    if (index === -1) {
        return path;
    }

    index = path.indexOf('/', index + 2);
    return path.slice(index + 1);
}

// Form
const file_full_name = document.getElementById('file-full-name');
const python_cover_image = document.getElementById('python-cover-image');
const python_hover_image = document.getElementById('python-hover-image');
const file_selected = document.getElementById('file-selected');
const submit = document.getElementById('submit-data');
const game_name = document.getElementById('game-name');
const console_select = document.getElementById('console-select');
const invalid_data = document.getElementById('invalid-data');

async function make_submit_work() {
    submit.addEventListener('click', async () => {   
        if ((game_name.value) && (console_select.value) && (getFileLocation(cover_preview.src) != 'web/images/placeholder.svg')) {
            // Removes the "Current ROM: " portion
            rom = file_full_name.innerText;
            full_cover_image = python_cover_image.innerText;
            full_hover_image = python_hover_image.innerText;

            if (getFileLocation(hover_preview.src) == 'web/images/placeholder.svg') {
                const hover_override = await eel.copy_cover_to_hover()();
                console.log(hover_override);

                setTimeout(() => {
                    eel.create_data(rom, game_name.value, console_select.value, cover_preview.src, hover_override, full_cover_image, full_hover_image);
                }, 250)
            } else {
                eel.create_data(rom, game_name.value, console_select.value, cover_preview.src, hover_preview.src, full_cover_image, full_hover_image);
            }

            setTimeout( () => {
                if (submit.getAttribute('data-entry-type') == 'unidentified') {
                    eel.cycle_unidentified_roms()();
                } else if (submit.getAttribute('data-entry-type') == 'missing') {
                    eel.cycle_missing_roms()();
                }
            }, 500)

        } else {
            invalid_data.classList.add('visible');
    
            setTimeout(() => {
                invalid_data.classList.remove('visible');
            }, 1500)
        }
    })
}

// Changes the current file and resets the form
eel.expose(next_unidentified_entry);
function next_unidentified_entry(new_rom) {
    console.log(new_rom);
    file_full_name.innerText = new_rom;
    file_selected.innerText = 'Current ROM: ' + new_rom.substring(new_rom.lastIndexOf('/') + 1);
    game_name.value = '';
    console_select.value = '3ds';
    cover_preview.src = 'images/placeholder.svg';
    hover_preview.src = 'images/placeholder.svg';
}


eel.expose(next_missing_entry);
function next_missing_entry(new_rom, rom_name, rom_console, rom_py_cover, rom_js_cover, rom_py_hover, rom_js_hover) {
    document.getElementById('header2').innerText = 'missing some data';
    submit.setAttribute('data-entry-type', 'missing');

    file_full_name.innerText = new_rom;
    file_selected.innerText = 'Current ROM: ' + new_rom.substring(new_rom.lastIndexOf('/') + 1);
    
    game_name.value = rom_name;
    game_name.setAttribute('readonly', true);

    console_select.value = rom_console;
    console_select.setAttribute('disabled', true);

    python_cover_image.innerText = rom_py_cover;
    cover_preview.src = rom_js_cover;

    python_hover_image.innerText = rom_py_hover;
    hover_preview.src = rom_js_hover;
}


// Closes the window once all ROMs are complete
eel.expose(close_entry_window);
function close_entry_window() {
    setTimeout(() => {
        window.close();
    }, 1000);
}

window.addEventListener('load', () => {
    window.resizeTo(900, 1111);
    window.moveTo(1500, 0);
    make_submit_work();

    setTimeout(() => {
        eel.entry_page_ready();
    }, 500)
})