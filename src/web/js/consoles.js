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