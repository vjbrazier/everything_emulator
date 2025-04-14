// Page Elements
const webpage = document.getElementById('webpage');
webpage.setAttribute('data-theme', localStorage.getItem('theme') || 'light');

const loading_bar  = document.getElementById('inner-loading-bar');
const progress     = document.getElementById('progress');
const current_file = document.getElementById('current-file');


// Sets the percentage of the loading bar
function set_loading_bar(percentage) {
    loading_bar.style.width = percentage + '%';
}

// Updates the page info following a ROM being hashed
eel.expose(update_info);
function update_info(rom, total) {
    current = parseInt(progress.innerText.substring(0, progress.innerText.indexOf('/')));
    current += 1;

    if (current == total + 1) {
        eel.reroute_to_main();
        window.close();
    }

    progress.innerText = `${current}/${total}: ${(current / total * 100).toFixed(0)}%`;
    set_loading_bar(current / total * 100);

    let rom_text = rom.substring(rom.lastIndexOf('/') + 1);
    current_file.innerText = rom_text;
    
    current_file.innerText = rom_text;

    return true; // Eel expects a return, this is just doing that for the sake of it
}

// To make the data not be returned a promise, it must bounce around functions
async function initialize_data() {
    roms = await eel.load_rom_files()();
    total = await eel.count_new_roms()();

    if (total == 0) {
        setTimeout(() => {
            eel.reroute_to_main();
            window.close();
        }, 500);
    }

    progress.innerText = '0/' + total + ': 0%';

    rom_text = roms[0].substring(String(roms[0]).lastIndexOf('/') + 1);

    current_file.innerText = rom_text;

    eel.rom_analysis();
}

window.onload = () => {
    initialize_data();
}