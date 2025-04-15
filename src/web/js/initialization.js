/* 
This file initalizes and creates the various elements of the page.
Elements: consoles, games
*/

// Containers for consoles and games
let games    = document.getElementById('games');
// let consoles = document.getElementById('consoles');

// Uses the console data from eel to create the console buttons
async function loadConsoles() {
    let console_list = await eel.get_consoles()();

    // Sets the limit for how far it can scroll and calculates the position
    console_pos_limit = console_list.length;
    calculate_consoles_per_scroll();

    // Creates the following elements for each console:
    // div    - Holds all elements to allow styling as a whole
    // button - Opens the console and shows image
    // text   - The name of the console
    // path  - The icon at the top-right of each console
    for (let i = 0; i < console_list.length; i++) {
        // Name is for appearance, id is for data-grabbing
        let console_name = console_list[i].replaceAll('-', ' ');
        let console_id   = console_name.replaceAll(' ', '-').toLowerCase()

        // Creation
        let console_div = document.createElement('div');
        let console_button = document.createElement('button');
        let console_text = document.createElement('h3');
        let console_path = document.createElement('h3');
        
        // Div
        console_div.classList.add('console-div');
        console_div.id = console_id + '-div';
        console_path.id = console_id + '-path';

        // Button
        console_button.classList.add('console-button');
        console_button.id = console_id;
        console_button.style.backgroundImage = "url('images/consoles/" + console_id + ".png')"

        // Text
        console_text.classList.add('console-text');
        console_text.innerText = capitalize(console_name);

        // Path
        console_path.classList.add('console-path');
        console_path.innerText = '🗁';

        // Appending to the page
        console_div.appendChild(console_button);
        console_div.appendChild(console_text);
        console_div.appendChild(console_path);
        consoles.appendChild(console_div);
    }

    //Called at the end, to ensure the paths aren't added before loaded
    addConsolePaths();
}


// Uses the game data from eel to create the game buttons
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
        game_button.classList.add('game-button');
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


// Waits for the page to load prior to creating the data 
window.onload = () => { 
    window.moveTo(0, 0);
    loadConsoles();
    loadGames();
}