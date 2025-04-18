/* 
This file initalizes and creates the various elements of the page.
*/
eel.expose(close_main_window)
function close_main_window() {
    eel.change_main_window_status();

    setTimeout(() => {
        window.close();
    }, 1000)
    
}

eel.expose(reload_main_window)
function reload_main_window() {
    window.location.reload();
}

// Waits for the page to load prior to creating the data 
window.addEventListener('load', () => {
    window.moveTo(0, 0);
    window.resizeTo(1500, 1080);
    loadConsoles();
    loadGames();
})