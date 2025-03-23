// Variables/Site Elements
const consoles                = document.getElementById('consoles');
const consoles_margin_initial = parseInt(window.getComputedStyle(consoles).marginLeft);
let   consoles_margin         = parseInt(window.getComputedStyle(consoles).marginLeft);
const consoles_left_limit   = consoles_margin_initial  + (450 * consoles.length);
const consoles_right_limit   = consoles_margin_initial - (450 * consoles.length);

const games              = document.getElementById('games');

// Creates all of the consoles
async function loadConsoles() {

    let console_list = await eel.get_consoles()();

    function createConsoles() {
        for (let i = 0; i < console_list.length; i++) {
            console_class = console_list[i].replaceAll(' ', '-').toLowerCase();
    
            var console_div    = document.createElement('div');
            var console_button = document.createElement('button');
            var console_text   = document.createElement('h3');
    
            console_div.classList.add('console-div');
            console_button.classList.add('console');
            console_text.classList.add('console-text');
    
            console_div.classList.add(console_class + '-div');
            console_button.classList.add(console_class);
            console_text.classList.add(console_class + '-text');
    
            console_button.innerText = console_list[i];
            console_text.innerText   = console_list[i];
    
            console_div.appendChild(console_button);
            console_div.appendChild(console_text);
            consoles.appendChild(console_div);
        }
    }

    // Makes a "looping" effect
    for (let i = 0; i < 5; i++) {
        createConsoles();
    }
}

document.getElementById('console-left').addEventListener('click', () => {
    if (consoles_margin != consoles_margin_initial) {
        consoles_margin += 450;
        consoles.style.marginLeft = consoles_margin + 'px';
    }
})

document.getElementById('console-right').addEventListener('click', () => {
    consoles_margin -= 450;
    consoles.style.marginLeft = consoles_margin + 'px';
})

// Loads up all the games
async function loadGames() {
    let game_list = await eel.get_games()();

    for (let i = 0; i < game_list.length; i++) {
        game_id = game_list[i].replaceAll(' ', '-').toLowerCase();

        var game_div     = document.createElement('div');
        var game_button  = document.createElement('button');
        var game_text    = document.createElement('h3');
        var game_console = document.createElement('h3');

        game_div.id     = game_id + '-div';
        game_button.id  = game_id;
        game_text.id    = game_id + '-text';
        game_console.id = game_id + '-div';

        game_div.classList.add('game-div');
        game_button.classList.add('game');
        game_text.classList.add('game-text');
        game_console.classList.add('game-console');

        game_button.innerText  = game_list[i];
        game_text.innerText    = game_list[i];
        game_console.innerText = 'Console';

        game_div.appendChild(game_button);
        game_div.appendChild(game_console);
        game_div.appendChild(game_text);
        games.appendChild(game_div);
    }
}

// Calls necessary functions once the page has loaded
document.addEventListener('DOMContentLoaded', () => {
    loadConsoles();
    loadGames();
})