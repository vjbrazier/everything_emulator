// Page Elements
const loading_bar  = document.getElementById('loading-bar');
const progress     = document.getElementById('progress');
const current_file = document.getElementById('current-file');

// Gets a list of roms
let roms = await eel.load_roms_files()();

// Gets how many new roms there are
let total = await eel.count_hashing(roms)();

// Sets up the loading page based on the info acquired
progress.innerText = '0/' + total;
current_file.innerText = roms[0];

for (let i = 0; i < roms.length; i++) {
    
}