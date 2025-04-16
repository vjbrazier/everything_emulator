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
        cover_preview.src = 'https://placehold.co/300x300';
    }
})

hover.addEventListener('click', async function () {
    const file = await eel.pick_image('hover')();

    if (file) {
        hover_preview.src = file;
    } else {
        hover_preview.src = 'https://placehold.co/300x300';
    }
})

// Form
const file_selected = document.getElementById('file-selected');
const submit = document.getElementById('submit-data');
const game_name = document.getElementById('game-name');
const console_select = document.getElementById('console-select');
const invalid_data = document.getElementById('invalid-data');

function make_submit_work() {
    submit.addEventListener('click', () => {   
        if ((game_name.value) && (console_select.value) && (cover_preview.src != 'https://placehold.co/300x300')) {
            // Removes the "Current ROM: " portion
            rom = file_selected.innerText.substring(file_selected.innerText.indexOf(':') + 2)
            
            if (hover_preview.src == 'https://placehold.co/300x300') {
                eel.create_data(rom, game_name.value, console_select.value, cover_preview.src, cover_preview.src);
            } else {
                eel.create_data(rom, game_name.value, console_select.value, cover_preview.src, hover_preview.src);
            }

            eel.cycle_rom()();
        } else {
            invalid_data.classList.add('visible');
    
            setTimeout(() => {
                invalid_data.classList.remove('visible');
            }, 1500)
        }
    })
}

// Changes the current file and resets the form
eel.expose(next_entry);
function next_entry(new_rom) {
    console.log(new_rom);
    file_selected.innerText = 'Current ROM: ' + new_rom.substring(new_rom.indexOf('/') + 1);
    game_name.value = '';
    console_select.value = '3ds';
    cover_preview.src = 'https://placehold.co/300x300';
    hover_preview.src = 'https://placehold.co/300x300';
}

// Closes the window once all ROMs are complete
eel.expose(close_window);
function close_window() {
    setTimeout(() => {
        window.close();
    }, 1000);
}

window.addEventListener('load', () => {
    window.resizeTo(900, 1100);
    window.moveTo(1500, 0);
    make_submit_work();
    eel.page_ready();
})