// Variables/Site Elements
const consoles                = document.getElementById('consoles');
const consoles_margin_initial = parseInt(window.getComputedStyle(consoles).marginLeft);
let   consoles_margin         = parseInt(window.getComputedStyle(consoles).marginLeft);
let   console_pos, console_pos_initial, console_pos_limit;
const games              = document.getElementById('games');

// Calculates the size of the screen and adjusts values accordingly for various screen sizes.
function calculate_consoles_per_scroll() {
    var window_width = window.innerWidth - 120;
    var count = 0;

    while (window_width - 450 > 0) {
        count++;
        window_width -= 450;
    }

    console_pos_initial = count;
    return count;
}

window.addEventListener('resize', () => {
    console_pos = calculate_consoles_per_scroll();
});

// Creates all of the consoles
async function loadConsoles() {
    let console_list = await eel.get_consoles()();

    console_pos_limit = console_list.length;
    console_pos = calculate_consoles_per_scroll(console_list);

    for (let i = 0; i < console_list.length; i++) {
        var console_name = console_list[i].replaceAll(' ', '-').toLowerCase();
        var current_console = document.createElement('button');
        
        current_console.classList.add('console-button');
        current_console.innerText = console_name;
        current_console.id = console_name;
        current_console.style.backgroundImage = "url('" + console_name + ".png')"

        consoles.appendChild(current_console);
    }


}

document.getElementById('console-left').addEventListener('click', () => {
    if (console_pos != console_pos_initial) {
        console_pos--;
        consoles_margin += 450;
        consoles.style.marginLeft = consoles_margin + 'px';
    }
})

document.getElementById('console-right').addEventListener('click', () => {
    if (console_pos != console_pos_limit) {
        console_pos++;
        consoles_margin -= 450;
        consoles.style.marginLeft = consoles_margin + 'px';
    }

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
        game_console.id = game_id + '-console';

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
window.onload = () => { 
    loadConsoles();
    loadGames();
}