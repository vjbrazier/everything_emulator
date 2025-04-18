/* 
Manages functions related to the console buttons.
Functions: opening console, setting filepath, changing filepath 
*/

// Adds the call to eel needed on each button to make it open files
async function addConsolePaths() {
    let console_buttons = document.getElementsByClassName('console-button');
    let console_paths   = document.getElementsByClassName('console-path');

    // The console buttons have an extra check for first time setup of one vs opening it
    for (let i = 0; i < console_buttons.length; i++) {
        console_buttons[i].addEventListener('click', async () => {
            let console_id = console_buttons[i].id;

            let is_emulator_setup = await eel.check_path_exists(console_id)();

            if (!is_emulator_setup) {
                eel.modify_console_path(console_id);
            } else {
                eel.open_console(console_id);
            }
        })
    }

    // The path button always just has you change the path
    for (let i = 0; i < console_paths.length; i++) {
        console_paths[i].addEventListener('click', async () => {
            let console_id = console_buttons[i].id;

            eel.modify_console_path(console_id);
        })
    }
}

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
    // path   - The icon at the top-right of each console
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