/* 
Manages functions related to the console buttons.
Functions: opening console, setting filepath, changing filepath 
*/

// Adds the call to eel needed on each button to make it open files
async function addConsolePaths() {
    const console_buttons = document.getElementsByClassName('console-button');

    for (let i = 0; i < console_buttons.length; i++) {
        console_buttons[i].addEventListener('click', async () => {
            let console_id = console_buttons[i].id;
            let emulator_setup = await eel.open_console(console_id)();

            if (!emulator_setup) {
                eel.user_console_selection(console_id);
            }
        })
    }
}