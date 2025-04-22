/*
Manages functions related to the game buttons.
Functions: 
*/
const games = document.getElementById('games');
let filtered = [];

async function loadGames() {
    let game_data = await eel.get_game_data()();

    for (let key in game_data) {
        let rom = game_data[key]

        let game_name    = rom['display-name'];
        let console_name = rom['console'];
        let cover_image  = rom['js-cover-image'];
        let hover_image  = rom['js-hover-image'];
        
        let game_div     = document.createElement('div');
        let game_button  = document.createElement('button');
        let game_text    = document.createElement('h3');
        let game_console = document.createElement('h3');
        let game_delete  = document.createElement('h3');
        let cover_img    = document.createElement('img');
        let hover_img    = document.createElement('img');

        game_button.id  = key;
        game_console.id = console_name;

        game_div.classList.add('game-div');
        game_div.classList.add('visible');
        game_button.classList.add('game-button');
        game_text.classList.add('game-text');
        game_console.classList.add('game-console');
        game_delete.classList.add('game-delete');
        cover_img.classList.add('game-img', 'cover');
        hover_img.classList.add('game-img', 'hover');
        
        cover_img.src = cover_image;
        hover_img.src = hover_image;

        game_text.innerText = game_name;
        game_console.innerText = capitalize(console_name.replaceAll('-', ' '));
        game_delete.innerText = 'Delete'; 

        game_button.appendChild(cover_img);
        game_button.appendChild(hover_img);

        game_div.appendChild(game_button);
        game_div.appendChild(game_console);
        game_div.appendChild(game_delete);
        game_div.appendChild(game_text);
        games.appendChild(game_div);
    }

    const saved_scroll = localStorage.getItem('scroll_position');

    if (saved_scroll) {
        window.scrollTo(0, parseFloat(saved_scroll));
        localStorage.removeItem('scroll_position');
    }

    // Only calls these after the content is fully loaded
    add_delete_functionality();
    add_game_button_functionality();
    add_filter_functionality();
}

// Makes each of the Delete buttons functional
function add_delete_functionality() {
    const delete_buttons = document.getElementsByClassName('game-delete');
    const game_buttons   = document.getElementsByClassName('game-button');
    
    for (let i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].addEventListener('click', () => {
            localStorage.setItem('scroll_position', window.scrollY);

            eel.delete_entry(game_buttons[i].id)();
        })
    }
}

function add_game_button_functionality() {
    const game_buttons  = document.getElementsByClassName('game-button');
    const game_consoles = document.getElementsByClassName('game-console');

    for (let i = 0; i < game_buttons.length; i++) {
        game_buttons[i].addEventListener('click', () => {
            localStorage.setItem('scroll_position', window.scrollY);

            eel.start_game(game_buttons[i].id, game_consoles[i].id)();
        })
    }
}

function update_filter() {
    const games = document.getElementsByClassName('game-div');
    const consoles = document.getElementsByClassName('game-console');

    if (filtered.length === 0) {
        for (let i = 0; i < games.length; i++) {
            games[i].classList.add('visible');
        }

        return;
    }

    for (let i = 0; i < games.length; i++) {
        games[i].classList.remove('visible');
    }

    for (let i = 0; i < filtered.length; i++) {
        for (let j = 0; j < games.length; j++) {
            if (consoles[j].id == filtered[i]) {
                games[j].classList.add('visible');
            }
        }
    }
}

function add_filter_functionality() {
    const console_filters = document.getElementsByClassName('console-filter');

    for (let i = 0; i < console_filters.length; i++) {
        console_filters[i].addEventListener('click', () => {
            console_filter = console_filters[i].dataset.id;
            
            if (console_filters[i].classList.contains('enabled')) {
                console.log('hello');
                console_filters[i].classList.remove('enabled');
                filtered.splice(filtered.indexOf(console_filter), 1);
                update_filter();
            }

            else {
                console_filters[i].classList.add('enabled');
                filtered.push(console_filter);
                update_filter();
            }
        })
    }
}

eel.expose(game_open_error);
function game_open_error(error, console_name) {
    const alert_box = document.getElementById("custom-alert");
    const alert_message = document.getElementById("alert-message");

    if (console_name) {
        alert_message.innerText = error + capitalize(console_name).replaceAll('-', ' ');
    } else {
        alert_message.innerText = error;
    }

    alert_box.classList.remove("hidden");
}

function close_alert() {
    document.getElementById("custom-alert").classList.add("hidden");
}

function search_games(search) {
    const game_divs = document.getElementsByClassName('game-div');
    const game_text = document.getElementsByClassName('game-text');

    if (search == '') {
        for (let i = 0; i < game_divs.length; i++) {
            game_divs[i].classList.add('visible');
        }

        return;
    }

    for (let i = 0; i < game_text.length; i++) {
        // game_name = game_text[i].innerText;
        // console.log(game_name);

        if (game_text[i].innerText.toLowerCase().includes(search)) {
            game_divs[i].classList.add('visible');
        } else {
            game_divs[i].classList.remove('visible');
        }

    }
}

document.getElementById('search-bar').addEventListener('input', (e) => {
    const search = e.target.value.toLowerCase();

    console.log(search);

    search_games(search);
})