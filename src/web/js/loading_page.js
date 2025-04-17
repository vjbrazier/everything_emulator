// Page Elements
const webpage = document.getElementById('webpage');
webpage.setAttribute('data-theme', localStorage.getItem('theme') || 'light');

const loading_bar  = document.getElementById('inner-loading-bar');
const progress     = document.getElementById('progress');
const current_file = document.getElementById('current-file');

// Timer showing how long the process is taking
let start_time = Date.now();
const time_elapsed = document.getElementById('time-elapsed');

setInterval(() => {
    const elapsed_seconds = Math.floor((Date.now() - start_time) / 1000);

    const minutes = Math.floor(elapsed_seconds / 60);
    const seconds = elapsed_seconds % 60;

    time_elapsed.textContent = `Time elapsed: ${minutes}:${seconds.toString().padStart(2, '0')}`;
}, 1000);

// Sets the percentage of the loading bar
function set_loading_bar(percentage) {
    loading_bar.style.width = percentage + '%';
}

// Adds the previous ROM to the list of finished ROMs
eel.expose(add_rom);
function add_rom(rom, found) {
    let rom_text = rom.substring(rom.lastIndexOf('/') + 1);
    current_file.innerText = 'Current file: ' + rom_text;

    let text = document.createElement('h3');
    
    if (found) {
        text.innerText = rom_text + ' ✓';
    } else {
        text.innerText = rom_text + ' ✗';
    }
    document.getElementById('files').appendChild(text);
}

let current = 0;

// Updates the page info following a ROM being hashed
eel.expose(update_info);
function update_info(rom, total, first_time) {
    let rom_text = rom.substring(rom.lastIndexOf('/') + 1);
    current_file.innerText = 'Current file: ' + rom_text;

    // Without this check, it will start at 1, not 0
    if (!first_time) {
        current++;
    }

    progress.innerText = `${current}/${total}: ${(current / total * 100).toFixed(0)}%`;
    set_loading_bar(current / total * 100);

    if (current == total) {
        eel.reroute_to_main();

        // Just a small delay prior to closing
        setTimeout(() => {
            window.close();
        }, 1000);
    }
}

// To make the data not be returned a promise, it must bounce around functions
async function initialize_data() {
    roms = await eel.load_new_rom_files()();
    total = roms.length;

    if (total == 0) {
        eel.reroute_to_main();

        setTimeout(() => {
            window.close();
        }, 1000);
    }

    progress.innerText = '0/' + total + ': 0%';
    set_loading_bar(0);

    rom_text = roms[0].substring(String(roms[0]).lastIndexOf('/') + 1);

    eel.rom_analysis();
}

window.onload = () => {
    initialize_data();
    window.resizeTo(1500, 1080)
}