// Variables/Site Elements
const consoles                = document.getElementById('consoles');
let   consoles_margin         = parseInt(window.getComputedStyle(consoles).marginLeft);
let   console_pos, console_pos_initial, console_pos_limit;
const games              = document.getElementById('games');

//Capitalizes a word for convenience
function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

// Calculates the size of the screen and adjusts values accordingly for various screen sizes.
function calculate_consoles_per_scroll() {
    var window_width = window.innerWidth - 120;
    var count = 0;

    while (window_width - 450 > 0) {
        count++;
        window_width -= 450;
    }

    //This is used to figure out how much the position changed by on resize
    var original_pos = console_pos_initial - count;

    console_pos_initial = count;

    //If console_pos hasn't been set yet (first load) it defaults it
    if (!console_pos) {
        console_pos = count;
    } else {
        console_pos = (console_pos - original_pos);
    }
}

//Changes your current position in the console list based on how many your screen size holds
window.addEventListener('resize', () => {
    calculate_consoles_per_scroll();
    document.getElementById('ratio').innerText = window.innerWidth + " x " + window.innerHeight;
});

// Creates all of the consoles
async function loadConsoles() {
    let console_list = await eel.get_consoles()();

    console_pos_limit = console_list.length;
    calculate_consoles_per_scroll(console_list);

    for (let i = 0; i < console_list.length; i++) {
        var console_name = console_list[i];
        var console_id   = console_name.replaceAll(' ', '-').toLowerCase()

        var console_div = document.createElement('div');
        var console_button = document.createElement('button');
        var console_text = document.createElement('h3');
        
        console_div.classList.add('console-div');
        console_div.id = console_id + '-div';

        console_button.classList.add('console-button');
        console_button.id = console_id;
        console_button.style.backgroundImage = "url('images/" + console_id + ".png')"

        console_text.classList.add('console-text');
        console_text.innerText = capitalize(console_name);

        console_div.appendChild(console_button);
        console_div.appendChild(console_text);

        consoles.appendChild(console_div);
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